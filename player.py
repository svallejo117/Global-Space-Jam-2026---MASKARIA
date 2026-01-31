# Maskaria: Guardianes Nasa - Jugador: volar, nadar, ver secretos, abrir puertas

import pygame
from config import (
    SCREEN_W, SCREEN_H, TILE_SIZE, GRAVITY, MAX_FALL,
    WATER_GRAVITY, WATER_MAX_FALL, FLY_LIFT, FLY_MAX_UP,
    SWIM_SPEED_UP, SWIM_SPEED_DOWN, DEFAULT_MASK,
    COYOTE_TIME, JUMP_BUFFER,
)
from masks import (
    get_jump_power, get_move_speed, get_mask_color, get_mask_animal_es,
    can_fly, can_swim, can_see_secrets, can_open_doors,
    can_double_jump, can_dash, can_speed, can_strong, can_shield,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE * 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.mask_id = DEFAULT_MASK  # None = sin máscara
        self.collected_masks = set()
        if DEFAULT_MASK:
            self.collected_masks.add(DEFAULT_MASK)
        self.invincible_frames = 0
        self.jumps_left = 1
        self.shield_available = True  # Máscara Escudo: una vez por vida
        self.dash_cooldown = 0
        self.in_water = False
        self._standing_height = TILE_SIZE * 2
        self.ground_grace_frames = 0  # coyote time
        self.jump_pressed_buffer = 0   # jump buffer
        self.just_landed = False
        self.apply_mask_stats()

    def apply_mask_stats(self):
        self._jump_power = get_jump_power(self.mask_id) if self.mask_id else 11.0
        self._move_speed = get_move_speed(self.mask_id) if self.mask_id else 4.0
        self._fly = can_fly(self.mask_id) if self.mask_id else False
        self._swim = can_swim(self.mask_id) if self.mask_id else False
        self._see_secrets = can_see_secrets(self.mask_id) if self.mask_id else False
        self._open_doors = can_open_doors(self.mask_id) if self.mask_id else False
        self._double_jump = can_double_jump(self.mask_id) if self.mask_id else False
        self._dash = can_dash(self.mask_id) if self.mask_id else False
        self._speed = can_speed(self.mask_id) if self.mask_id else False
        self._strong = can_strong(self.mask_id) if self.mask_id else False
        self._shield = can_shield(self.mask_id) if self.mask_id else False

    def set_mask(self, mask_id):
        if mask_id == self.mask_id:
            return
        self.mask_id = mask_id
        if mask_id:
            self.collected_masks.add(mask_id)
        self.apply_mask_stats()
        self.jumps_left = 1

    def collect_mask(self, mask_id):
        if mask_id:
            self.collected_masks.add(mask_id)
        self.set_mask(mask_id)

    def jump(self):
        if self.on_ground or self.ground_grace_frames > 0:
            self.vel_y = -self._jump_power
            self.on_ground = False
            self.ground_grace_frames = 0
            self.jumps_left = 2 if self._double_jump else 1
            return True
        if self._double_jump and self.jumps_left > 0:
            self.vel_y = -self._jump_power
            self.jumps_left -= 1
            return True
        return False

    def request_jump_buffer(self):
        """Llama cuando el jugador pulsa salto; si aterriza pronto, salta."""
        self.jump_pressed_buffer = JUMP_BUFFER

    def update(self, platforms, breakables, water_rects, use_hidden, hidden_platforms, dt=1):
        # Evitar TypeError si argumentos en orden incorrecto (bool donde se espera lista)
        if isinstance(hidden_platforms, bool):
            use_hidden = hidden_platforms
            hidden_platforms = []
        if isinstance(platforms, bool):
            platforms = []
        self.apply_mask_stats()
        if self.invincible_frames > 0:
            self.invincible_frames -= 1

        self.in_water = False
        for wr in water_rects:
            if self.rect.colliderect(wr):
                self.in_water = True
                break

        keys = pygame.key.get_pressed()
        in_water_with_swim = self.in_water and self._swim
        in_air_flying = not self.on_ground and not self.in_water and self._fly and keys[pygame.K_UP]

        if in_water_with_swim:
            self.vel_x = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vel_x -= self._move_speed * 0.8
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vel_x += self._move_speed * 0.8
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.vel_y = SWIM_SPEED_UP
            elif keys[pygame.K_DOWN]:
                self.vel_y = SWIM_SPEED_DOWN
            else:
                self.vel_y = self.vel_y * 0.9
            self.vel_y = max(-8, min(8, self.vel_y))
            self.facing_right = self.vel_x >= 0 if self.vel_x != 0 else self.facing_right
        elif in_air_flying:
            self.vel_y = max(self.vel_y - FLY_LIFT, FLY_MAX_UP)
            move = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move += 1
            self.vel_x = move * self._move_speed
            if move != 0:
                self.facing_right = move > 0
        else:
            move = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move += 1
            self.vel_x = move * self._move_speed
            if move != 0:
                self.facing_right = move > 0
            if not self.in_water:
                self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL)
            else:
                self.vel_y = min(self.vel_y + WATER_GRAVITY, WATER_MAX_FALL)

        self.rect.x += int(self.vel_x)
        self._resolve_horizontal(platforms, hidden_platforms, use_hidden)

        was_on_ground = self.on_ground
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self._resolve_vertical(platforms, hidden_platforms, use_hidden)

        self.just_landed = self.on_ground and not was_on_ground
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.on_ground:
            self.ground_grace_frames = 0
            self.jumps_left = 2 if self._double_jump else 1
            if self.jump_pressed_buffer > 0:
                self.vel_y = -self._jump_power
                self.on_ground = False
                self.jump_pressed_buffer = 0
        else:
            if was_on_ground:
                self.ground_grace_frames = COYOTE_TIME
            elif self.ground_grace_frames > 0:
                self.ground_grace_frames -= 1
        if self.jump_pressed_buffer > 0:
            self.jump_pressed_buffer -= 1

    def _resolve_horizontal(self, platforms, hidden_platforms, use_hidden):
        # Evitar TypeError si por error se pasa bool en lugar de lista (ej. argumentos en orden incorrecto)
        if isinstance(platforms, bool):
            platforms = []
        if isinstance(hidden_platforms, bool):
            hidden_platforms = []
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right
                self.vel_x = 0
        if use_hidden:
            for p in hidden_platforms:
                if self.rect.colliderect(p.rect):
                    if self.vel_x > 0:
                        self.rect.right = p.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = p.rect.right
                    self.vel_x = 0

    def _resolve_vertical(self, platforms, hidden_platforms, use_hidden):
        if isinstance(platforms, bool):
            platforms = []
        if isinstance(hidden_platforms, bool):
            hidden_platforms = []
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    # Subir desde el agua (o salto): colocar pies sobre la plataforma para poder salir
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
        if use_hidden:
            for p in hidden_platforms:
                if self.rect.colliderect(p.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.bottom = p.rect.top
                        self.vel_y = 0
                        self.on_ground = True

    def is_invincible_to_traps(self):
        return self.invincible_frames > 0

    def sees_secrets(self):
        return self._see_secrets

    def can_open_doors(self):
        return self._open_doors

    def can_shield(self):
        return self._shield and self.shield_available

    def use_shield(self):
        if self._shield and self.shield_available:
            self.shield_available = False
            self.invincible_frames = 90
            return True
        return False

    def draw(self, surface, camera_x=0):
        from draw_mask import draw_character_as_animal, draw_mask_oval
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)
        inv_flash = self.invincible_frames > 0 and self.invincible_frames % 6 < 3
        if self.mask_id:
            # Con máscara: te conviertes en la forma y color del animal de esa máscara
            mask_color = get_mask_color(self.mask_id)
            animal_es = get_mask_animal_es(self.mask_id)
            draw_character_as_animal(
                surface, r, mask_color, animal_es,
                facing_right=self.facing_right,
                invincible_flash=inv_flash,
            )
        else:
            # Sin máscara: cuerpo humanoide + cara base (tono piel)
            body = pygame.Rect(r.x + 4, r.y + r.h // 2 - 4, r.w - 8, r.h // 2 + 4)
            body_color = (100, 85, 75)
            if inv_flash:
                body_color = (255, 255, 255)
            pygame.draw.rect(surface, body_color, body)
            pygame.draw.rect(surface, (70, 60, 55), body, 1)
            head_rect = pygame.Rect(r.x + 2, r.y - 2, r.w - 4, r.h // 2 + 8)
            skin = (255, 255, 255) if inv_flash else (200, 170, 150)
            draw_mask_oval(surface, head_rect, skin, glow=False, eyes=True)
