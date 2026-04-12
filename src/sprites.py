
# ASTEROIDE SINGLEPLAYER v1.0
# This file defines the interactive game entities and their local behaviors.

import math
from random import random, uniform, choice

import pygame as pg

import config as C
from utils import Vec, angle_to_vec, draw_circle, draw_poly, wrap_pos


class Bullet(pg.sprite.Sprite):
    # Initialize a player bullet with position, velocity, and lifetime.
    def __init__(self, pos: Vec, vel: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.ttl = C.BULLET_TTL
        self.r = C.BULLET_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def update(self, dt: float):
        # Move the bullet, wrap it on screen, and expire it over time.
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        # Draw the bullet on the target surface.
        draw_circle(surf, self.pos, self.r)


class UfoBullet(pg.sprite.Sprite):
    # Initialize a UFO bullet with position, velocity, and lifetime.
    def __init__(self, pos: Vec, vel: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.ttl = C.UFO_BULLET_TTL
        self.r = C.BULLET_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def update(self, dt: float):
        # Move the UFO bullet, wrap it on screen, and expire it over time.
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        # Draw the UFO bullet on the target surface.
        draw_circle(surf, self.pos, self.r)


class Asteroid(pg.sprite.Sprite):
    # Initialize an asteroid with its position, velocity, and size profile.
    def __init__(self, pos: Vec, vel: Vec, size: str):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.size = size
        self.r = C.AST_SIZES[size]["r"]
        self.volatile = random() < C.VOLATILE_CHANCE
        self.poly = self._make_poly()
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def _make_poly(self):
        # Build an irregular polygon outline based on the asteroid size.
        steps = 12 if self.size == "L" else 10 if self.size == "M" else 8
        pts = []
        for i in range(steps):
            ang = i * (360 / steps)
            jitter = uniform(0.75, 1.2)
            r = self.r * jitter
            v = Vec(math.cos(math.radians(ang)),
                    math.sin(math.radians(ang)))
            pts.append(v * r)
        return pts

    def update(self, dt: float):
        # Move the asteroid and wrap it across the screen.
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        # Draw the asteroid outline on the target surface.
        pts = [(self.pos + p) for p in self.poly]
        color = C.RED if getattr(self, "volatile", False) else C.WHITE
        pg.draw.polygon(surf, color, pts, width=1)


class Ship(pg.sprite.Sprite):
    # Initialize the player ship and its gameplay state.
    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        self.angle = -90.0
        self.cool = 0.0
        self.invuln = 0.0
        self.alive = True
        self.r = C.SHIP_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        
        # New mechanics
        self.dash_cool = 0.0
        self.dash_active = 0.0
        self.spread_timer = 0.0
        self.has_shield = False

    def control(self, keys: pg.key.ScancodeWrapper, dt: float):
        # Apply rotation, thrust, and friction from the current input state.
        if keys[pg.K_LEFT]:
            self.angle -= C.SHIP_TURN_SPEED * dt
        if keys[pg.K_RIGHT]:
            self.angle += C.SHIP_TURN_SPEED * dt
        if keys[pg.K_UP]:
            self.vel += angle_to_vec(self.angle) * C.SHIP_THRUST * dt
        self.vel *= C.SHIP_FRICTION

    def fire(self) -> list[Bullet]:
        # Spawn player bullets when the fire cooldown allows it.
        if self.cool > 0:
            return []
        
        dirv = angle_to_vec(self.angle)
        pos = self.pos + dirv * (self.r + 6)
        
        bullets = []
        if self.spread_timer > 0:
            for offset_ang in [-15, 0, 15]:
                d = angle_to_vec(self.angle + offset_ang)
                vel = self.vel + d * C.SHIP_BULLET_SPEED
                bullets.append(Bullet(pos, vel))
        else:
            vel = self.vel + dirv * C.SHIP_BULLET_SPEED
            bullets.append(Bullet(pos, vel))
            
        self.cool = C.SHIP_FIRE_RATE
        return bullets

    def dash(self) -> bool:
        # Dash forward with invulnerability
        if self.dash_cool <= 0:
            self.dash_active = getattr(C, "DASH_DURATION", 0.25)
            self.dash_cool = getattr(C, "DASH_COOLDOWN", 2.0)
            dirv = angle_to_vec(self.angle)
            
            val_speed = getattr(C, "DASH_SPEED", C.SHIP_THRUST * getattr(C, "DASH_SPEED_MULT", 3.5)) * 1.6
            self.vel = dirv * val_speed
            self.invuln = self.dash_active
            return True
        return False

    def update(self, dt: float):
        # Advance cooldowns, move the ship, and wrap it on screen.
        if self.cool > 0:
            self.cool -= dt
        if self.invuln > 0:
            self.invuln -= dt
            
        if self.dash_cool > 0:
            self.dash_cool -= dt
        if self.dash_active > 0:
            self.dash_active -= dt
            if self.dash_active <= 0:
                # Brake dramatically so we don't crash after dash
                if self.vel.length() > C.SHIP_THRUST:
                    self.vel = self.vel.normalize() * (C.SHIP_THRUST * 0.5)
                # Give a brief invulnerability window after dash ends
                self.invuln = 0.4
            
        if self.spread_timer > 0:
            self.spread_timer -= dt
            
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        # Draw the ship and its temporary invulnerability indicator.
        dirv = angle_to_vec(self.angle)
        left = angle_to_vec(self.angle + 140)
        right = angle_to_vec(self.angle - 140)
        p1 = self.pos + dirv * self.r
        p2 = self.pos + left * self.r * 0.9
        p3 = self.pos + right * self.r * 0.9
        draw_poly(surf, [p1, p2, p3])
        if self.invuln > 0 and int(self.invuln * 10) % 2 == 0:
            draw_circle(surf, self.pos, self.r + 6)
            
        if self.has_shield:
            pg.draw.circle(surf, C.BLUE, self.pos, self.r + 10, width=2)


class UFO(pg.sprite.Sprite):
    # Initialize a UFO enemy with its size profile and movement state.
    def __init__(self, pos: Vec, small: bool):
        super().__init__()
        self.pos = Vec(pos)
        self.small = small
        profile = C.UFO_SMALL if small else C.UFO_BIG
        self.r = profile["r"]
        self.aim = profile["aim"]
        self.speed = C.UFO_SPEED
        self.cool = C.UFO_FIRE_EVERY
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        self.dir = Vec(1, 0) if uniform(0, 1) < 0.5 else Vec(-1, 0)

    def update(self, dt: float):
        # Move the UFO, advance its fire cooldown, and remove it off screen.
        self.pos += self.dir * self.speed * dt
        self.cool -= dt
        if self.pos.x < -self.r * 2 or self.pos.x > C.WIDTH + self.r * 2:
            self.kill()
        self.rect.center = self.pos

    def fire_at(self, target_pos: Vec) -> UfoBullet | None:
        # Fire a bullet toward the ship with accuracy based on the UFO type.
        if self.cool > 0:
            return None
        aim_vec = Vec(target_pos) - self.pos
        if aim_vec.length_squared() == 0:
            aim_vec = self.dir.normalize()
        else:
            aim_vec = aim_vec.normalize()
        max_error = (1.0 - self.aim) * 60.0
        shot_dir = aim_vec.rotate(uniform(-max_error, max_error))
        self.cool = C.UFO_FIRE_EVERY
        spawn_pos = self.pos + shot_dir * (self.r + 6)
        vel = shot_dir * C.UFO_BULLET_SPEED
        return UfoBullet(spawn_pos, vel)

    def draw(self, surf: pg.Surface):
        # Draw the UFO body on the target surface.
        w, h = self.r * 2, self.r
        rect = pg.Rect(0, 0, w, h)
        rect.center = self.pos
        pg.draw.ellipse(surf, C.WHITE, rect, width=1)
        cup = pg.Rect(0, 0, w * 0.5, h * 0.7)
        cup.center = (self.pos.x, self.pos.y - h * 0.3)
        pg.draw.ellipse(surf, C.WHITE, cup, width=1)


class PowerUp(pg.sprite.Sprite):
    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.type = choice(["SHIELD", "SPREAD"])
        self.r = 10
        self.ttl = C.POWERUP_TTL
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def update(self, dt: float):
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        color = C.BLUE if self.type == "SHIELD" else C.GREEN
        pg.draw.circle(surf, color, self.pos, self.r, width=2)


class Anomaly(pg.sprite.Sprite):
    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.max_r = C.ANOMALY_HORIZON_R
        self.r = 1.0  # Começa pequena
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        self.time = 0.0
        self.ttl = 15.0  # Vive por 15 segundos

    def update(self, dt: float):
        self.time += dt
        self.ttl -= dt
        
        # Cresce lenta e constantemente nos primeiros 8.0 segundos
        if self.time < 8.0:
            self.r = 1.0 + (self.max_r - 1.0) * (self.time / 8.0)
        # Encolhe suavemente no último 1 segundo
        elif self.ttl < 1.0:
            self.r = max(0.1, self.max_r * self.ttl)
        else:
            self.r = self.max_r
            
        if self.ttl <= 0:
            self.kill()
            
        self.rect.width = self.r * 2
        self.rect.height = self.r * 2
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        if self.r > 2.0:
            r_pulse = self.r + math.sin(self.time * 5.0) * 3.0
            pg.draw.circle(surf, C.PURPLE, self.pos, max(1, int(r_pulse)), width=2)
