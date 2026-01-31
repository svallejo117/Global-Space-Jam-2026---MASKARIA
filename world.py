# Maskaria: Guardianes Nasa - Mundo: agua, puertas, plataformas ocultas, enemigos que sueltan máscaras, NPCs

import math
import pygame
import random
from config import TILE_SIZE, MASK_COLORS
from masks import get_mask_color, get_mask_animal_es, get_all_mask_ids


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=1, h=1, color=(120, 90, 60), top_grass=False):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, h * TILE_SIZE)
        self.color = color
        self.w, self.h = w, h
        self.top_grass = top_grass

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        dark = (max(0, self.color[0] - 35), max(0, self.color[1] - 25), max(0, self.color[2] - 20))
        light = (min(255, self.color[0] + 25), min(255, self.color[1] + 20), min(255, self.color[2] + 15))
        pygame.draw.rect(surface, dark, r)
        pygame.draw.rect(surface, light, (r.x, r.y, r.w, max(2, r.h // 4)))
        pygame.draw.line(surface, light, (r.x, r.y), (r.x, r.bottom), 2)
        pygame.draw.line(surface, (60, 45, 35), (r.x, r.bottom - 1), (r.right, r.bottom - 1), 2)
        if self.top_grass and self.rect.height >= TILE_SIZE:
            grass_r = pygame.Rect(r.x, r.y, r.w, min(8, r.h))
            pygame.draw.rect(surface, (70, 130, 70), grass_r)
            pygame.draw.rect(surface, (90, 150, 85), (r.x, r.y, r.w, 3))
            for i in range(0, r.w, 8):
                pygame.draw.line(surface, (50, 110, 55), (r.x + i, r.y + 4), (r.x + i + 4, r.y + 8), 1)


class HiddenPlatform(pygame.sprite.Sprite):
    """Solo visible si el jugador tiene la máscara Ver secretos."""
    def __init__(self, x, y, w=1, h=1):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, h * TILE_SIZE)
        self.color = (160, 120, 230)
        self.pulse = 0

    def draw(self, surface, camera_x=0, visible=False):
        if not visible:
            return
        self.pulse = (self.pulse + 0.08) % (2 * math.pi)
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        glow = (min(255, self.color[0] + 40), min(255, self.color[1] + 30), min(255, self.color[2] + 50))
        pygame.draw.rect(surface, (max(0, self.color[0] - 30), max(0, self.color[1] - 25), max(0, self.color[2] - 20)), r)
        pygame.draw.rect(surface, glow, (r.x, r.y, r.w, max(4, r.h // 4)))
        pygame.draw.rect(surface, (140, 100, 210), r, 2)
        pygame.draw.line(surface, (200, 180, 255), (r.x, r.y + 2), (r.right, r.y + 2), 1)


class Water(pygame.sprite.Sprite):
    """Agua: sin máscara Nadar ahogas; con máscara nadas."""
    def __init__(self, x, y, w=1, h=1):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, h * TILE_SIZE)
        self.w, self.h = w, h
        self.wave = 0

    def update(self):
        self.wave = (self.wave + 0.2) % (2 * math.pi)

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        for row in range(self.h):
            for col in range(self.w):
                rr = pygame.Rect(r.x + col * TILE_SIZE, r.y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                shift = int(2 * math.sin(self.wave + col * 0.5 + row * 0.3))
                rr.y += shift
                dark = (35, 95, 160)
                mid = (50, 130, 200)
                light = (80, 170, 230)
                pygame.draw.rect(surface, dark, rr)
                pygame.draw.rect(surface, mid, (rr.x, rr.y, rr.w, rr.h // 2))
                pygame.draw.line(surface, light, (rr.x, rr.y + 2), (rr.right, rr.y + 2), 1)
                if (col + row) % 3 == 0:
                    bx, by = rr.x + rr.w // 2 + int(4 * math.sin(self.wave + col)), rr.y + rr.h // 2
                    pygame.draw.circle(surface, (255, 255, 255), (bx, by), 2)


class Door(pygame.sprite.Sprite):
    """Puerta normal: al tocarla cambias de sala."""
    def __init__(self, x, y, w=1, h=2, target_room=None, spawn_x=0, spawn_y=0):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, h * TILE_SIZE)
        self.target_room = target_room
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.locked = False

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        pts = [(r.x, r.bottom), (r.right, r.bottom), (r.right - 8, r.y + 8), (r.x + 8, r.y + 8)]
        pygame.draw.polygon(surface, (50, 130, 80), pts)
        pygame.draw.polygon(surface, (70, 180, 110), [(r.x + 10, r.bottom - 4), (r.right - 10, r.bottom - 4), (r.right - 14, r.y + 14), (r.x + 14, r.y + 14)])
        pygame.draw.polygon(surface, (40, 100, 60), pts, 2)
        font = pygame.font.Font(None, 22)
        label = "¡META!" if self.target_room == "victory" else "SALIDA"
        text = font.render(label, 1, (255, 255, 255))
        surface.blit(text, (r.x + r.w // 2 - text.get_width() // 2, r.y + r.h // 2 - 10))


class LockedDoor(pygame.sprite.Sprite):
    """Puerta sellada: necesitas máscara Abrir puertas + E para abrir."""
    def __init__(self, x, y, w=1, h=2, target_room=None, spawn_x=0, spawn_y=0):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, h * TILE_SIZE)
        self.target_room = target_room
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, (120, 100, 60), r)
        pygame.draw.rect(surface, (80, 60, 30), r, 3)
        font = pygame.font.Font(None, 22)
        text = font.render("CERRADA", 1, (255, 220, 100))
        surface.blit(text, (r.x + r.w // 2 - text.get_width() // 2, r.y + r.h // 2 - 8))


class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, w=1):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, TILE_SIZE)
        self.w = w

    def update(self):
        pass

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, (60, 55, 70), r)
        for i in range(self.w):
            cx = r.x + i * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.polygon(surface, (180, 50, 50), [
                (cx, r.bottom - 4), (cx - 8, r.bottom), (cx, r.bottom - 12), (cx + 8, r.bottom),
            ])


class FallingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=2):
        super().__init__()
        self.rect = pygame.Rect(x, y, w * TILE_SIZE, TILE_SIZE)
        self.w = w
        self.falling = False
        self.vel_y = 0
        self.stand_delay = 35

    def update(self):
        if self.falling:
            self.vel_y = min(self.vel_y + 0.5, 12)
            self.rect.y += int(self.vel_y)

    def trigger(self):
        if not self.falling:
            self.falling = True

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        color = (140, 100, 60) if not self.falling else (100, 70, 50)
        pygame.draw.rect(surface, color, r)
        pygame.draw.rect(surface, (90, 60, 30), r, 2)


class MovingHazard(pygame.sprite.Sprite):
    def __init__(self, x, y, range_x=0, range_y=0, speed=2):
        super().__init__()
        self.size = TILE_SIZE
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.x1, self.x2 = x, x + range_x
        self.y1, self.y2 = y, y + range_y
        self.vertical = range_y > 0
        self.speed = speed
        self.t = 0.0

    def update(self):
        self.t += 0.02
        if self.vertical:
            self.rect.y = int(self.y1 + (self.y2 - self.y1) * (0.5 + 0.5 * math.sin(self.t * self.speed)))
        else:
            self.rect.x = int(self.x1 + (self.x2 - self.x1) * (0.5 + 0.5 * math.sin(self.t * self.speed)))

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        pygame.draw.circle(surface, (220, 80, 60), (r.x + r.w // 2, r.y + r.h // 2), r.w // 2 - 2)
        for i in range(8):
            angle = self.t + i * math.pi / 4
            ex = r.x + r.w // 2 + int(12 * math.cos(angle))
            ey = r.y + r.h // 2 + int(12 * math.sin(angle))
            pygame.draw.line(surface, (180, 60, 40), (r.x + r.w // 2, r.y + r.h // 2), (ex, ey), 2)


class Mummy(pygame.sprite.Sprite):
    """Momia: patrulla y hace daño; al pisarla muere pero no suelta máscara."""
    def __init__(self, x, y, patrol_range=64):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.mask_id = None
        self.x1 = x
        self.x2 = x + patrol_range
        self.vel_x = 2

    def update(self, platforms):
        self.rect.x += self.vel_x
        if self.rect.x <= self.x1:
            self.rect.x = self.x1
            self.vel_x = 2
        if self.rect.x >= self.x2:
            self.rect.x = self.x2
            self.vel_x = -2
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                    self.vel_x = -2
                else:
                    self.rect.left = p.rect.right
                    self.vel_x = 2
                break

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        # Cuerpo: vendas blanquecinas
        body = pygame.Rect(r.x + 2, r.y + 4, r.w - 4, r.h - 4)
        pygame.draw.rect(surface, (240, 230, 210), body)
        pygame.draw.rect(surface, (200, 190, 175), body, 1)
        # Franjas de venda
        for i in range(0, r.w - 4, 6):
            pygame.draw.line(surface, (220, 210, 195), (r.x + 2 + i, r.y + 6), (r.x + 2 + i, r.bottom - 4), 1)
        # Ojos verdes
        pygame.draw.circle(surface, (60, 180, 80), (r.x + 10, r.y + 14), 3)
        pygame.draw.circle(surface, (60, 180, 80), (r.x + 22, r.y + 14), 3)
        pygame.draw.circle(surface, (30, 90, 40), (r.x + 10, r.y + 14), 1)
        pygame.draw.circle(surface, (30, 90, 40), (r.x + 22, r.y + 14), 1)


class Crab(pygame.sprite.Sprite):
    """Cangrejo: patrulla y hace daño; al pisarlo muere pero no suelta máscara."""
    def __init__(self, x, y, patrol_range=48):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.mask_id = None
        self.x1 = x
        self.x2 = x + patrol_range
        self.vel_x = 2
        self.t = 0

    def update(self, platforms):
        self.rect.x += self.vel_x
        self.t += 0.15
        if self.rect.x <= self.x1:
            self.rect.x = self.x1
            self.vel_x = 2
        if self.rect.x >= self.x2:
            self.rect.x = self.x2
            self.vel_x = -2
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                    self.vel_x = -2
                else:
                    self.rect.left = p.rect.right
                    self.vel_x = 2
                break

    def draw(self, surface, camera_x=0):
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        # Caparazón rojo/naranja
        body = pygame.Rect(r.x + 4, r.y + 6, r.w - 8, r.h - 10)
        pygame.draw.ellipse(surface, (200, 80, 60), body)
        pygame.draw.ellipse(surface, (150, 50, 40), body, 1)
        # Pinzas (se mueven con t)
        pinch = 4 + int(2 * math.sin(self.t))
        pygame.draw.line(surface, (200, 80, 60), (r.x + 4, r.y + 16), (r.x - 2, r.y + 16 + pinch), 3)
        pygame.draw.line(surface, (200, 80, 60), (r.right - 4, r.y + 16), (r.right + 2, r.y + 16 + pinch), 3)
        pygame.draw.circle(surface, (220, 100, 70), (r.x + 8, r.y + 18), 4)
        pygame.draw.circle(surface, (220, 100, 70), (r.right - 8, r.y + 18), 4)
        # Ojos
        pygame.draw.circle(surface, (40, 30, 20), (r.x + 10, r.y + 10), 3)
        pygame.draw.circle(surface, (40, 30, 20), (r.right - 10, r.y + 10), 3)


class Enemy(pygame.sprite.Sprite):
    """Enemigo que patrulla; al pisarlo suelta la máscara que lleva (si tiene)."""
    def __init__(self, x, y, mask_id, patrol_range=64):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.mask_id = mask_id
        self.x1 = x
        self.x2 = x + patrol_range
        self.vel_x = 2
        self.color = get_mask_color(mask_id) if mask_id else (180, 60, 80)

    def update(self, platforms):
        self.rect.x += self.vel_x
        if self.rect.x <= self.x1:
            self.rect.x = self.x1
            self.vel_x = 2
        if self.rect.x >= self.x2:
            self.rect.x = self.x2
            self.vel_x = -2
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                    self.vel_x = -2
                else:
                    self.rect.left = p.rect.right
                    self.vel_x = 2
                break

    def draw(self, surface, camera_x=0):
        from draw_mask import draw_character_as_animal
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        # Enemigo dibujado como el animal de su máscara y su color
        animal_es = get_mask_animal_es(self.mask_id) if self.mask_id else None
        if animal_es:
            draw_character_as_animal(surface, r, self.color, animal_es, facing_right=(self.vel_x >= 0), invincible_flash=False)
        else:
            body = pygame.Rect(r.x + 2, r.y + r.h // 2 - 2, r.w - 4, r.h // 2 + 2)
            pygame.draw.rect(surface, (70, 55, 60), body)
            pygame.draw.rect(surface, (55, 45, 50), body, 1)
            from draw_mask import draw_mask_oval
            head = pygame.Rect(r.x + 2, r.y, r.w - 4, r.h // 2 + 4)
            draw_mask_oval(surface, head, self.color, glow=False, eyes=True)


class NPC(pygame.sprite.Sprite):
    """NPC que te da una máscara al interactuar (E)."""
    def __init__(self, x, y, mask_id, message="¡Toma mi máscara!"):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE * 2)
        self.mask_id = mask_id
        self.message = message
        self.given = False
        self.bob = 0

    def update(self):
        self.bob = (self.bob + 0.15) % (2 * math.pi)

    def draw(self, surface, camera_x=0):
        from draw_mask import draw_mask_oval
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y + int(4 * math.sin(self.bob)), self.rect.w, self.rect.h)
        body_color = (180, 200, 160) if not self.given else (100, 100, 100)
        pygame.draw.rect(surface, body_color, (r.x + 4, r.y + r.h // 3, r.w - 8, r.h * 2 // 3))
        pygame.draw.rect(surface, (140, 160, 120) if not self.given else (80, 80, 80), (r.x + 4, r.y + r.h // 3, r.w - 8, r.h * 2 // 3), 1)
        if self.mask_id and not self.given:
            head = pygame.Rect(r.x + 2, r.y + 4, r.w - 4, r.h // 3 + 4)
            draw_mask_oval(surface, head, get_mask_color(self.mask_id), glow=True, eyes=False)
        font = pygame.font.Font(None, 22)
        txt = "¡Listo!" if self.given else "E"
        t = font.render(txt, 1, (255, 255, 255))
        surface.blit(t, (r.x + r.w // 2 - t.get_width() // 2, r.y + r.h - 18))


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE // 2, TILE_SIZE // 2)
        self.bob = 0
        self.color = (255, 220, 80)

    def update(self):
        self.bob = (self.bob + 0.2) % (2 * math.pi)

    def draw(self, surface, camera_x=0):
        dy = int(3 * math.sin(self.bob))
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y + dy, self.rect.w, self.rect.h)
        cx, cy = r.x + r.w // 2, r.y + r.h // 2
        pygame.draw.circle(surface, self.color, (cx, cy), r.w)
        pygame.draw.circle(surface, (200, 180, 50), (cx, cy), r.w, 1)


class MaskPickup(pygame.sprite.Sprite):
    """Máscara en el suelo (recogida o soltada por enemigo)."""
    def __init__(self, x, y, mask_id):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.mask_id = mask_id
        self.color = get_mask_color(mask_id) if mask_id else (200, 200, 200)
        self.bob = 0

    def update(self):
        self.bob = (self.bob + 0.15) % (2 * math.pi)

    def draw(self, surface, camera_x=0):
        from draw_mask import draw_character_as_animal
        dy = int(5 * math.sin(self.bob))
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y + dy, self.rect.w, self.rect.h)
        # Máscara en el suelo: forma del animal y color para identificarla
        animal_es = get_mask_animal_es(self.mask_id) if self.mask_id else None
        if animal_es:
            draw_character_as_animal(surface, r, self.color, animal_es, facing_right=True, invincible_flash=False)
        else:
            from draw_mask import draw_mask_oval
            draw_mask_oval(surface, r, self.color, glow=True, eyes=True)


class WordPickup(pygame.sprite.Sprite):
    """Palabra coleccionable en Nasa Yuwe: al tocarla se añade al diccionario."""
    def __init__(self, x, y, word_id):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.word_id = word_id
        self.bob = 0

    def update(self):
        self.bob = (self.bob + 0.12) % (2 * math.pi)

    def draw(self, surface, camera_x=0):
        dy = int(4 * math.sin(self.bob))
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y + dy, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, (255, 240, 180), r)
        pygame.draw.rect(surface, (200, 160, 80), r, 2)
        font = pygame.font.Font(None, 20)
        t = font.render("?", 1, (80, 60, 40))
        surface.blit(t, (r.x + r.w // 2 - t.get_width() // 2, r.y + r.h // 2 - 8))


def build_world_from_grid(grid, room_data=None):
    """Construye el mundo desde la rejilla. room_data: doors, enemy_masks, npcs."""
    room_data = room_data or {}
    platforms = pygame.sprite.Group()
    hidden_platforms = pygame.sprite.Group()
    water = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    locked_doors = pygame.sprite.Group()
    mask_pickups = pygame.sprite.Group()
    word_pickups = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    falling = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    npcs = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    start_x, start_y = TILE_SIZE * 2, 0

    enemy_masks = room_data.get("enemy_masks", {})  # (tx, ty) -> mask_id
    npc_list = room_data.get("npcs", [])  # [{"x": tx, "y": ty, "mask_id": id, "message": "..."}]
    door_list = room_data.get("doors", [])  # [{"x": tx, "y": ty, "target": room_id, "spawn_x": px, "spawn_y": py, "locked": bool}]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            px, py = x * TILE_SIZE, y * TILE_SIZE
            key = (x, y)
            if cell == "#":
                top_grass = (y == 0 or (y > 0 and x < len(row) and grid[y - 1][x] != "#"))
                platforms.add(Platform(px, py, 1, 1, (120, 90, 60), top_grass=top_grass))
            elif cell == "X":
                hidden_platforms.add(HiddenPlatform(px, py, 1, 1))
            elif cell == "W":
                water.add(Water(px, py, 1, 1))
            elif cell == "S":
                spikes.add(Spikes(px, py, 1))
            elif cell == "F":
                falling.add(FallingPlatform(px, py, 2))
            elif cell == "H":
                hazards.add(MovingHazard(px, py, TILE_SIZE * 4, 0, 1.5))
            elif cell == "V":
                hazards.add(MovingHazard(px, py, 0, TILE_SIZE * 3, 1.2))
            elif cell == "N":
                mask_id = enemy_masks.get(key) if key in enemy_masks else (get_all_mask_ids()[0] if get_all_mask_ids() else None)
                enemies.add(Enemy(px, py, mask_id, TILE_SIZE * 4))
            elif cell == "U":
                enemies.add(Mummy(px, py, TILE_SIZE * 4))
            elif cell == "K":
                enemies.add(Crab(px, py, TILE_SIZE * 3))
            elif cell == "C":
                coins.add(Coin(px + TILE_SIZE // 4, py + TILE_SIZE // 4))
            elif cell == "P":
                # Jugador 2 tiles alto: rect.y = techo de plataforma - 2*tile para que los pies estén sobre la plataforma
                start_x, start_y = px, py - TILE_SIZE * 2
            elif cell == "M":
                mask_id = room_data.get("mask_pickup_at", {}).get(key)
                if mask_id:
                    mask_pickups.add(MaskPickup(px, py, mask_id))

    for d in door_list:
        tx, ty = d.get("x", 0) * TILE_SIZE, d.get("y", 0) * TILE_SIZE
        tw, th = d.get("w", 1), d.get("h", 2)
        target = d.get("target", "")
        sx = d.get("spawn_x", tx)
        sy = d.get("spawn_y", ty + 100)
        if d.get("locked", False):
            ld = LockedDoor(tx, ty, tw, th, target, sx, sy)
            locked_doors.add(ld)
        else:
            dr = Door(tx, ty, tw, th, target, sx, sy)
            doors.add(dr)

    for n in npc_list:
        nx = n.get("x", 0) * TILE_SIZE
        ny = n.get("y", 0) * TILE_SIZE
        mask_id = n.get("mask_id")
        msg = n.get("message", "¡Toma mi máscara!")
        npcs.add(NPC(nx, ny, mask_id, msg))

    all_platforms = list(platforms) + list(hidden_platforms)  # hidden count for collision when visible
    return {
        "platforms": platforms,
        "hidden_platforms": hidden_platforms,
        "water": water,
        "doors": doors,
        "locked_doors": locked_doors,
        "mask_pickups": mask_pickups,
        "word_pickups": word_pickups,
        "spikes": spikes,
        "falling": falling,
        "hazards": hazards,
        "enemies": enemies,
        "npcs": npcs,
        "coins": coins,
        "start_x": start_x,
        "start_y": start_y,
    }
