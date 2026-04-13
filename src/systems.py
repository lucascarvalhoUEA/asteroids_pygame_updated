
# ASTEROIDE SINGLEPLAYER v1.0
# This file coordinates world state, spawning, collisions, scoring, and progression.

import math
from random import uniform, random, choice

import pygame as pg

import config as C
from sprites import Asteroid, Ship, UFO, PowerUp, Anomaly, UfoBullet
from utils import Vec, rand_edge_pos, rand_unit_vec


class World:
    # Initialize the world state, entity groups, timers, and player progress.
    def __init__(self):
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2))
        self.bullets = pg.sprite.Group()
        self.ufo_bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.anomalies = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group(self.ship)
        self.anomaly_timer = uniform(15.0, 30.0)
        self.combo = 0
        self.combo_timer = 0.0
        self.dash_uses = 0
        
        self.score = 0
        self.lives = C.START_LIVES
        self.wave = 0
        self.wave_cool = C.WAVE_DELAY
        self.safe = C.SAFE_SPAWN_TIME
        self.ufo_timer = C.UFO_SPAWN_EVERY
        self.game_over = False  # Sinaliza fim de jogo para a cena principal

    def start_wave(self):
        # Spawn a new asteroid wave with difficulty based on the current round.
        self.wave += 1
        self.ship.has_shield = False
        self.dash_uses = 0
        count = 3 + self.wave
        for _ in range(count):
            pos = rand_edge_pos()
            while (pos - self.ship.pos).length() < 150:
                pos = rand_edge_pos()
            ang = uniform(0, math.tau)
            speed = uniform(C.AST_VEL_MIN, C.AST_VEL_MAX)
            vel = Vec(math.cos(ang), math.sin(ang)) * speed
            self.spawn_asteroid(pos, vel, "L")

    def spawn_asteroid(self, pos: Vec, vel: Vec, size: str):
        # Create an asteroid and register it in the world groups.
        a = Asteroid(pos, vel, size)
        self.asteroids.add(a)
        self.all_sprites.add(a)

    def spawn_ufo(self):
        # Spawn a single UFO at a screen edge and send it across the playfield.
        if self.ufos:
            return
        small = uniform(0, 1) < 0.5
        y = uniform(0, C.HEIGHT)
        x = 0 if uniform(0, 1) < 0.5 else C.WIDTH
        ufo = UFO(Vec(x, y), small)
        ufo.dir.xy = (1, 0) if x == 0 else (-1, 0)
        self.ufos.add(ufo)
        self.all_sprites.add(ufo)

    def ufo_try_fire(self):
        # Let every active UFO attempt to fire at the ship.
        for ufo in self.ufos:
            bullet = ufo.fire_at(self.ship.pos)
            if bullet:
                self.ufo_bullets.add(bullet)
                self.all_sprites.add(bullet)

    def try_fire(self):
        # Fire a player bullet when the bullet cap allows it.
        if len(self.bullets) >= C.MAX_BULLETS:
            return
        bullets = self.ship.fire()
        for b in bullets:
            self.bullets.add(b)
            self.all_sprites.add(b)

    def dash(self):
        # Trigger the directional dash if points available.
        cost = getattr(C, "DASH_BASE_COST", 50) * (self.dash_uses + 1)
        if self.score >= cost:
            if self.ship.dash():
                self.score -= cost
                self.dash_uses += 1

    def update(self, dt: float, keys):
        # Update the world simulation, timers, enemy behavior, and progression.
        self.ship.control(keys, dt)
        self.all_sprites.update(dt)
        if self.safe > 0:
            self.safe -= dt
            self.ship.invuln = 0.5
            
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo = 0
                
        if self.ufos:
            self.ufo_try_fire()
        else:
            self.ufo_timer -= dt
        if not self.ufos and self.ufo_timer <= 0:
            self.spawn_ufo()
            self.ufo_timer = C.UFO_SPAWN_EVERY

        # Gravity logic
        for anomaly in self.anomalies:
            for spr in list(self.all_sprites):
                if spr == anomaly:
                    continue
                diff = anomaly.pos - spr.pos
                dist_sq = diff.length_squared()
                if dist_sq > 0:
                    # O poder gravitacional escala de acordo com o tamanho atual da anomalia
                    scale_factor = anomaly.r / 10.0
                    force = (C.ANOMALY_GRAVITY_PULL * scale_factor) / dist_sq
                    if hasattr(spr, "vel"):
                        spr.vel += diff.normalize() * force * dt

        self.handle_collisions()

        if not self.asteroids and self.wave_cool <= 0:
            self.start_wave()
            self.wave_cool = C.WAVE_DELAY
        elif not self.asteroids:
            self.wave_cool -= dt
            
        if self.wave >= C.ANOMALY_SPAWN_WAVE:
            self.anomaly_timer -= dt
            if self.anomaly_timer <= 0:
                pos = Vec(uniform(200, C.WIDTH-200), uniform(200, C.HEIGHT-200))
                an = Anomaly(pos)
                self.anomalies.add(an)
                self.all_sprites.add(an)
                self.anomaly_timer = uniform(15.0, 30.0)

    def handle_collisions(self):
        # PowerUp collisions with ship
        if self.ship.alive:
            for p in list(self.powerups):
                if (p.pos - self.ship.pos).length() < (p.r + self.ship.r):
                    if p.type == "SHIELD":
                        self.ship.has_shield = True
                    elif p.type == "SPREAD":
                        self.ship.spread_timer = C.POWERUP_SPREAD_DURATION
                    p.kill()

        # Anomaly eating logic
        for anomaly in list(self.anomalies):
            if not anomaly.alive():
                continue
            for spr in list(self.all_sprites):
                if spr == anomaly:
                    continue
                if (spr.pos - anomaly.pos).length() < anomaly.r:
                    if spr == self.ship:
                        hit = True
                        if self.ship.has_shield:
                            self.ship.has_shield = False
                            self.ship.invuln = 1.0
                            # Jump slightly away to not get stuck
                            self.ship.pos += (self.ship.pos - anomaly.pos).normalize() * 50
                        else:
                            self.ship_die()
                    elif not isinstance(spr, Anomaly):
                        spr.kill()

        # Resolve collisions between bullets, asteroids, UFOs, and the ship.
        hits = pg.sprite.groupcollide(
            self.asteroids,
            self.bullets,
            False,
            True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r,
        )
        for ast, _ in hits.items():
            self.split_asteroid(ast)

        ufo_hits = pg.sprite.groupcollide(
            self.asteroids,
            self.ufo_bullets,
            False,
            True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r,
        )
        for ast, _ in ufo_hits.items():
            self.split_asteroid(ast)

        if self.ship.invuln <= 0 and self.safe <= 0:
            hit = False
            for ast in self.asteroids:
                if (ast.pos - self.ship.pos).length() < (ast.r + self.ship.r):
                    hit = True
                    break
            if not hit:
                for ufo in self.ufos:
                    if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                        hit = True
                        break
            if not hit:
                for bullet in self.ufo_bullets:
                    if (bullet.pos - self.ship.pos).length() < (bullet.r + self.ship.r):
                        bullet.kill()
                        hit = True
                        break

            if hit:
                if self.ship.has_shield:
                    self.ship.has_shield = False
                    self.ship.invuln = 1.0
                else:
                    self.ship_die()

        for ufo in list(self.ufos):
            for b in list(self.bullets):
                if (ufo.pos - b.pos).length() < (ufo.r + b.r):
                    self.combo += 1
                    self.combo_timer = C.COMBO_TIMEOUT
                    mult = min(self.combo, C.MAX_MULTIPLIER)
                    
                    score = (C.UFO_SMALL["score"] if ufo.small
                             else C.UFO_BIG["score"])
                    self.score += score * mult
                    ufo.kill()
                    b.kill()

    def split_asteroid(self, ast: Asteroid):
        # Destroy an asteroid, award score, and spawn its smaller fragments.
        self.combo += 1
        self.combo_timer = C.COMBO_TIMEOUT
        multiplier = min(self.combo, C.MAX_MULTIPLIER)
        
        self.score += C.AST_SIZES[ast.size]["score"] * multiplier
        split = C.AST_SIZES[ast.size]["split"]
        pos = Vec(ast.pos)
        
        if getattr(ast, "volatile", False):
            for _ in range(C.VOLATILE_PROJECTIONS):
                dirv = rand_unit_vec()
                b = UfoBullet(pos, dirv * C.VOLATILE_PROJ_SPEED)
                self.ufo_bullets.add(b)
                self.all_sprites.add(b)
        else:
            for s in split:
                dirv = rand_unit_vec()
                speed = uniform(C.AST_VEL_MIN, C.AST_VEL_MAX) * 1.2
                self.spawn_asteroid(pos, dirv * speed, s)
                
        if random() < C.POWERUP_DROP_CHANCE and ast.size == "L":
            p = PowerUp(pos)
            self.powerups.add(p)
            self.all_sprites.add(p)
            
        ast.kill()

    def ship_die(self):
        # Remove uma vida; sinaliza game over ou reposiciona a nave.
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True  # Game.run() detecta e muda de cena
            return
        self.ship.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
        self.ship.vel.xy = (0, 0)
        self.ship.angle = -90
        self.ship.spread_timer = 0.0
        self.ship.invuln = C.SAFE_SPAWN_TIME
        self.safe = C.SAFE_SPAWN_TIME

    def draw(self, surf: pg.Surface, font: pg.font.Font):
        # Draw all world entities and the current HUD information.
        for spr in self.all_sprites:
            spr.draw(surf)

        pg.draw.line(surf, (60, 60, 60), (0, 50), (C.WIDTH, 50), width=1)
        txt = f"SCORE {self.score:06d}   LIVES {self.lives}   WAVE {self.wave}"
        
        # Display dash readiness and cost
        cost = getattr(C, "DASH_BASE_COST", 50) * (self.dash_uses + 1)
        if self.ship.dash_cool > 0:
            dash_status = f"{self.ship.dash_cool:.1f}s"
        elif self.score < cost:
            dash_status = f"NEED {cost}PTS"
        else:
            dash_status = f"READY (-{cost}PTS)"
            
        txt += f"   DASH: {dash_status}"
        
        if self.combo > 1:
            mult = min(self.combo, C.MAX_MULTIPLIER)
            txt += f"   COMBO x{mult}"
            
        label = font.render(txt, True, C.WHITE)
        surf.blit(label, (10, 10))
