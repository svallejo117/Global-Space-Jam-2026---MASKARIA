# MASKARIA - Efectos: sacudida de cámara y partículas

import random
import pygame
from config import TILE_SIZE


class ScreenShake:
    def __init__(self):
        self.duration = 0
        self.intensity = 0

    def trigger(self, duration=15, intensity=6):
        self.duration = max(self.duration, duration)
        self.intensity = max(self.intensity, intensity)

    def update(self):
        if self.duration > 0:
            self.duration -= 1

    def offset(self):
        if self.duration <= 0:
            return 0, 0
        return random.randint(-self.intensity, self.intensity), random.randint(-self.intensity, self.intensity)


class Particle:
    def __init__(self, x, y, vx, vy, color, life=30, size=4):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.life = life
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        self.vx *= 0.95
        self.vy *= 0.95

    def draw(self, surface, camera_x=0):
        if self.life <= 0:
            return
        r = pygame.Rect(int(self.x - camera_x), int(self.y), self.size, self.size)
        alpha = min(255, self.life * 8)
        s = pygame.Surface((self.size * 2, self.size * 2))
        s.set_alpha(alpha)
        s.fill(self.color)
        surface.blit(s, (r.x - self.size // 2, r.y - self.size // 2))


class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit_mask_pickup(self, x, y, color):
        for _ in range(12):
            a = random.uniform(0, 6.28)
            v = random.uniform(2, 6)
            self.particles.append(Particle(
                x + TILE_SIZE // 2, y + TILE_SIZE // 2,
                random.uniform(-3, 3), random.uniform(-6, -2),
                color, life=25, size=5
            ))

    def emit_block_break(self, x, y):
        color = (180, 120, 60)
        for _ in range(8):
            self.particles.append(Particle(
                x + TILE_SIZE // 2, y + TILE_SIZE // 2,
                random.uniform(-4, 4), random.uniform(-3, 0),
                color, life=20, size=4
            ))

    def emit_hurt(self, x, y):
        for _ in range(10):
            self.particles.append(Particle(
                x, y, random.uniform(-5, 5), random.uniform(-8, -2),
                (255, 80, 80), life=15, size=4
            ))

    def emit_landing(self, x, y):
        for _ in range(6):
            self.particles.append(Particle(
                x + TILE_SIZE // 2, y + TILE_SIZE * 2,
                random.uniform(-2, 2), random.uniform(0, 3),
                (200, 180, 140), life=12, size=3
            ))

    def emit_stomp(self, x, y, color):
        for _ in range(8):
            self.particles.append(Particle(
                x + TILE_SIZE // 2, y + TILE_SIZE // 2,
                random.uniform(-4, 4), random.uniform(-2, 4),
                color, life=18, size=4
            ))

    def emit_coin(self, x, y):
        for _ in range(5):
            self.particles.append(Particle(
                x, y, random.uniform(-2, 2), random.uniform(-4, -1),
                (255, 220, 80), life=20, size=3
            ))

    def emit_fly_trail(self, x, y, color):
        self.particles.append(Particle(
            x, y, random.uniform(-1, 1), random.uniform(0, 2),
            tuple(min(255, c + 80) for c in color[:3]), life=15, size=2
        ))

    def emit_sparkle(self, x, y, color=None):
        """Brillos dorados/violetas al recoger máscara."""
        c = color or (255, 220, 120)
        for _ in range(14):
            a = random.uniform(0, 6.28)
            v = random.uniform(2, 7)
            self.particles.append(Particle(
                x, y, v * __import__("math").cos(a), -v * __import__("math").sin(a) - 2,
                c, life=22, size=4
            ))

    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def draw(self, surface, camera_x=0):
        for p in self.particles:
            p.draw(surface, camera_x)
