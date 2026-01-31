# Maskaria: Guardianes Nasa - UI: HUD, pantallas, parallax, zone splash

import math
import pygame
from config import TILE_SIZE, SCREEN_W, ZONES, VERSION, HUD_PANEL_H, HUD_LEFT_W, HUD_CENTER_W
from masks import get_mask_name, get_mask_color, get_mask_desc, get_all_mask_ids, get_mask_name_nasa, get_mask_animal_es

# Colores del HUD (una sola barra superior)
_HUD_BG = (38, 33, 55)
_HUD_BORDER_TOP = (55, 48, 75)
_HUD_BORDER_V = (72, 65, 95)
_HUD_BORDER_BOTTOM = (95, 85, 125)
_HUD_LABEL = (145, 132, 175)
_HUD_SEP = (65, 58, 85)


def _draw_heart_icon(surface, center_x, center_y, size=10, color=(255, 80, 100), outline=(200, 50, 70)):
    """Dibuja un corazón rojo (gratuito, sin imagen). Dos lóbulos + punta."""
    cx, cy = center_x, center_y
    r = size // 2
    # Lóbulos superiores (círculos)
    pygame.draw.circle(surface, color, (cx - r, cy - r), r)
    pygame.draw.circle(surface, color, (cx + r, cy - r), r)
    # Punta inferior (triángulo que cierra el corazón)
    pts = [(cx - size, cy - r), (cx + size, cy - r), (cx, cy + size - 2)]
    pygame.draw.polygon(surface, color, pts)
    pygame.draw.circle(surface, outline, (cx - r, cy - r), r, 1)
    pygame.draw.circle(surface, outline, (cx + r, cy - r), r, 1)
    pygame.draw.polygon(surface, outline, pts, 1)


def draw_hud(surface, player, room_name, lives, coins=0, camera_x=0):
    """HUD: barra superior. Izq = máscara activa | Centro = sala | Der = monedas, vidas, 10 máscaras (teclas 1-0)."""
    from draw_mask import draw_mask_oval, draw_character_as_animal
    font = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 20)
    W = surface.get_width()
    panel_h = HUD_PANEL_H
    left_w = HUD_LEFT_W
    center_w = HUD_CENTER_W
    right_start = left_w + center_w
    line_h = 18
    icon_x, icon_y = 10, 18
    icon_sz = 28

    # Panel y separadores
    pygame.draw.rect(surface, _HUD_BG, (0, 0, W, panel_h))
    pygame.draw.line(surface, _HUD_BORDER_TOP, (0, 0), (W, 0), 2)
    pygame.draw.line(surface, _HUD_BORDER_V, (left_w, 0), (left_w, panel_h), 1)
    pygame.draw.line(surface, _HUD_BORDER_V, (right_start, 0), (right_start, panel_h), 1)
    pygame.draw.line(surface, _HUD_BORDER_BOTTOM, (0, panel_h), (W, panel_h), 2)

    # --- IZQUIERDA: Máscara activa ---
    surface.blit(font_small.render("Máscara activa", 1, _HUD_LABEL), (icon_x, 2))
    max_name_w = left_w - icon_x - icon_sz - 14
    if player.mask_id:
        mask_rect = pygame.Rect(icon_x, icon_y, icon_sz, icon_sz)
        draw_character_as_animal(surface, mask_rect, get_mask_color(player.mask_id), get_mask_animal_es(player.mask_id), facing_right=True, invincible_flash=False)
        full_name = get_mask_name(player.mask_id) + (" — " + get_mask_name_nasa(player.mask_id) if get_mask_name_nasa(player.mask_id) else "")
        if font_small.size(full_name)[0] > max_name_w:
            full_name = full_name[:24] + "…"
        surface.blit(font_small.render(full_name, 1, (255, 255, 255)), (icon_x + icon_sz + 8, 20))
        desc = get_mask_desc(player.mask_id)
        if desc:
            if font_small.size(desc)[0] > max_name_w:
                desc = desc[:38] + "…"
            surface.blit(font_small.render(desc, 1, (198, 192, 218)), (icon_x + icon_sz + 8, 20 + line_h))
    else:
        mask_rect = pygame.Rect(icon_x, icon_y, icon_sz, icon_sz)
        draw_mask_oval(surface, mask_rect, (115, 98, 92), glow=False, eyes=True)
        surface.blit(font_small.render("Sin máscara", 1, (222, 212, 202)), (icon_x + icon_sz + 8, 20))
        surface.blit(font_small.render("Pisa enemigos o habla con NPCs (E)", 1, (162, 156, 182)), (icon_x + icon_sz + 8, 20 + line_h))

    # --- CENTRO: Nombre de sala ---
    if font.size(room_name)[0] > center_w - 16:
        room_name = room_name[:32] + "…"
    level_text = font.render(room_name, 1, (242, 237, 255))
    cx = left_w + center_w // 2
    surface.blit(level_text, (cx - level_text.get_width() // 2, 20))

    # --- DERECHA: Monedas, vidas, Máscaras (1-0) ---
    rx = right_start + 12
    pygame.draw.circle(surface, (255, 222, 82), (rx + 8, 22), 8)
    pygame.draw.circle(surface, (255, 242, 200), (rx + 6, 20), 2)
    surface.blit(font_small.render(f"x{coins}", 1, (255, 232, 122)), (rx + 20, 14))
    rx += 52
    # Corazón rojo dibujado (no depende del carácter ♥ de la fuente)
    _draw_heart_icon(surface, rx + 10, 22, 10, color=(255, 80, 100), outline=(200, 50, 70))
    surface.blit(font.render(str(lives), 1, (255, 102, 122)), (rx + 22, 12))
    rx += 48
    pygame.draw.line(surface, _HUD_SEP, (rx, 8), (rx, panel_h - 8), 1)
    rx += 10
    surface.blit(font_small.render("Máscaras (1-0)", 1, _HUD_LABEL), (rx, 2))
    mask_ids = get_all_mask_ids()
    icon_w = 22
    for i, mid in enumerate(mask_ids):
        rr = pygame.Rect(rx + i * icon_w, 14, 20, 20)
        is_collected = mid in player.collected_masks
        is_equipped = player.mask_id == mid
        if is_collected:
            draw_character_as_animal(surface, rr, get_mask_color(mid), get_mask_animal_es(mid), facing_right=True, invincible_flash=False)
            if is_equipped:
                pygame.draw.rect(surface, (255, 255, 100), (rr.x - 1, rr.y - 1, rr.w + 2, rr.h + 2), 2)
        else:
            pygame.draw.rect(surface, (48, 44, 58), rr)
            pygame.draw.rect(surface, (68, 62, 78), rr, 1)
            q = font_small.render("?", 1, (92, 86, 102))
            surface.blit(q, (rr.x + rr.w // 2 - q.get_width() // 2, rr.y + rr.h // 2 - q.get_height() // 2))
        key_label = "0" if i == 9 else str(i + 1)
        num_color = (255, 255, 100) if is_equipped else (182, 177, 202)
        surface.blit(font_small.render(key_label, 1, num_color), (rr.x + rr.w // 2 - 4, 36))


def draw_title_screen(surface, font_large, font_small):
    """Pantalla de título: máscara ceremonial destacada, tema Nasa."""
    from draw_mask import draw_title_mask
    surface.fill((25, 22, 45))
    W, H = surface.get_width(), surface.get_height()
    # Máscara central grande (estilo ceremonial, más chevre)
    mask_rect = pygame.Rect(W // 2 - 64, H // 4 - 54, 128, 108)
    draw_title_mask(surface, mask_rect, (220, 180, 255), glow=True)
    title = font_large.render("Maskaria: Guardianes Nasa", 1, (255, 220, 140))
    sub = font_small.render("Máscaras de animales. Cada una te da un poder y la lengua Nasa Yuwe.", 1, (200, 180, 220))
    tw, th = title.get_size()
    surface.blit(title, (W // 2 - tw // 2, H // 3 + 60))
    surface.blit(sub, (W // 2 - sub.get_width() // 2, H // 3 + th + 72))
    sub2 = font_small.render("Rescata máscaras de enemigos (pisándolos) o recibe de NPCs (E).", 1, (170, 165, 200))
    surface.blit(sub2, (W // 2 - sub2.get_width() // 2, H // 3 + th + 96))
    ver = font_small.render(f"v{VERSION}", 1, (130, 125, 150))
    surface.blit(ver, (W - ver.get_width() - 16, 12))
    inst = font_small.render("ENTER o ESPACIO para comenzar", 1, (220, 210, 240))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 70))
    inst2 = font_small.render("Menú principal", 1, (160, 155, 180))
    surface.blit(inst2, (W // 2 - inst2.get_width() // 2, H - 48))


def draw_main_menu(surface, font_large, font_small, selected):
    """Menú principal: tema máscaras, icono junto a opción seleccionada."""
    from draw_mask import draw_mask_oval
    from masks import get_mask_color, get_all_mask_ids
    W, H = surface.get_width(), surface.get_height()
    for y in range(0, H + 8, 8):
        t = y / H
        c = (int(28 + t * 22), int(24 + t * 28), int(48 + t * 45))
        pygame.draw.rect(surface, c, (0, y, W, 8))
    # Pequeñas máscaras decorativas (las 4 del juego) — tema central
    mask_ids = get_all_mask_ids()
    for i, mid in enumerate(mask_ids):
        rx = W // 2 - 78 + i * 42
        rr = pygame.Rect(rx, 24, 32, 28)
        draw_mask_oval(surface, rr, get_mask_color(mid), glow=False, eyes=False)
    title = font_large.render("Maskaria: Guardianes Nasa", 1, (255, 240, 200))
    surface.blit(title, (W // 2 - title.get_width() // 2, 58))
    sub = font_small.render("Cada máscara es un animal y un poder. Aprende Nasa Yuwe.", 1, (190, 182, 220))
    surface.blit(sub, (W // 2 - sub.get_width() // 2, 94))
    items = ["JUGAR", "OPCIONES", "CRÉDITOS", "SALIR"]
    y0 = 200
    for i, item in enumerate(items):
        is_sel = i == selected
        color = (255, 255, 220) if is_sel else (200, 195, 220)
        txt = f"  {item}  " if is_sel else item
        t = font_small.render(txt, 1, color)
        tx = W // 2 - t.get_width() // 2
        ty = y0 + i * 52
        if is_sel:
            small_mask = pygame.Rect(tx - 32, ty - 4, 28, 28)
            draw_mask_oval(surface, small_mask, (200, 180, 255), glow=True, eyes=False)
        surface.blit(t, (tx, ty))
    inst = font_small.render("Flechas: Seleccionar   ENTER: Confirmar   ESC: Atrás", 1, (150, 145, 180))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 44))


def draw_level_select(surface, font_large, font_small, selected, level_options, unlocked):
    """Pantalla Elegir nivel: Continuar (donde quedaste) + Nivel 1 a 10. Bloqueados con candado."""
    W, H = surface.get_width(), surface.get_height()
    surface.fill((28, 25, 48))
    for y in range(0, H + 8, 8):
        t = y / H
        c = (int(30 + t * 20), int(26 + t * 22), int(50 + t * 40))
        pygame.draw.rect(surface, c, (0, y, W, 8))
    # Título
    title = font_large.render("NIVELES", 1, (255, 230, 140))
    surface.blit(title, (W // 2 - title.get_width() // 2, 36))
    sub = font_small.render("Continuar donde quedaste o elige un nivel.", 1, (190, 182, 220))
    surface.blit(sub, (W // 2 - sub.get_width() // 2, 88))
    # Lista: Continuar + Nivel 1..10
    y0 = 140
    line_h = 38
    for i, label in enumerate(level_options):
        is_sel = i == selected
        can_select = i in unlocked
        color = (255, 255, 200) if is_sel else ((200, 200, 220) if can_select else (100, 95, 120))
        txt = label if can_select else f"{label} (bloqueado)"
        t = font_small.render(txt, 1, color)
        tx = W // 2 - 180
        ty = y0 + i * line_h
        # Fondo del ítem
        if is_sel:
            pygame.draw.rect(surface, (55, 50, 80), (tx - 12, ty - 4, 360, line_h - 4), border_radius=6)
        if not can_select and i > 0:
            # Candado pequeño
            lock_x = tx + 340
            pygame.draw.rect(surface, (180, 80, 80), (lock_x, ty + 2, 14, 16), border_radius=2)
            pygame.draw.rect(surface, (220, 200, 100), (lock_x + 3, ty, 8, 6), border_radius=1)
        surface.blit(t, (tx, ty))
    inst = font_small.render("Flechas: Seleccionar   ENTER: Jugar   ESC: Menú", 1, (150, 145, 180))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 40))


def draw_pause_menu(surface, font_large, font_small, selected):
    """Menú de pausa: Continuar, Reiniciar, Palabras Nasa Yuwe, Menú principal."""
    from draw_mask import draw_mask_oval
    overlay = pygame.Surface((surface.get_width(), surface.get_height()))
    overlay.set_alpha(180)
    overlay.fill((20, 20, 40))
    surface.blit(overlay, (0, 0))
    W, H = surface.get_width(), surface.get_height()
    mask_r = pygame.Rect(W // 2 - 22, 78, 44, 38)
    draw_mask_oval(surface, mask_r, (180, 160, 220), glow=True, eyes=False)
    t = font_large.render("PAUSA", 1, (255, 240, 200))
    surface.blit(t, (W // 2 - t.get_width() // 2, 118))
    items = ["Continuar", "Reiniciar sala", "Palabras en Nasa Yuwe", "Menú principal"]
    y0 = 200
    for i, item in enumerate(items):
        color = (255, 255, 200) if i == selected else (180, 180, 200)
        txt = font_small.render(f"> {item}" if i == selected else item, 1, color)
        surface.blit(txt, (W // 2 - txt.get_width() // 2, y0 + i * 44))
    save_hint = font_small.render("Tu progreso se guarda al pasar puertas y al volver al menú.", 1, (120, 115, 140))
    surface.blit(save_hint, (W // 2 - save_hint.get_width() // 2, H - 70))
    inst = font_small.render("Flechas: Seleccionar   ENTER: Confirmar   ESC: Continuar", 1, (140, 140, 160))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 40))


def draw_glossary_screen(surface, font_large, font_small, unlocked_word_ids):
    """Diccionario Nasa Yuwe: Español → Nasa Yuwe. Solo palabras desbloqueadas."""
    from glossary import get_word_by_id
    overlay = pygame.Surface((surface.get_width(), surface.get_height()))
    overlay.set_alpha(200)
    overlay.fill((25, 22, 45))
    surface.blit(overlay, (0, 0))
    W, H = surface.get_width(), surface.get_height()
    title = font_large.render("Palabras en Nasa Yuwe", 1, (255, 240, 200))
    surface.blit(title, (W // 2 - title.get_width() // 2, 24))
    sub = font_small.render("Español  →  Nasa Yuwe (lengua del pueblo Nasa, Colombia)", 1, (160, 150, 200))
    surface.blit(sub, (W // 2 - sub.get_width() // 2, 58))
    y = 100
    line_h = 26
    font_w = pygame.font.Font(None, 22)
    words_to_show = []
    for wid in unlocked_word_ids:
        w = get_word_by_id(wid)
        if w:
            words_to_show.append(w)
    pad = 60
    for w in words_to_show:
        es_part = font_w.render(w["es"], 1, (255, 250, 230))
        arrow = font_w.render("  →  ", 1, (150, 140, 170))
        nasa_part = font_w.render(w["nasa"], 1, (220, 200, 255))
        surface.blit(es_part, (pad, y))
        surface.blit(arrow, (pad + es_part.get_width(), y))
        surface.blit(nasa_part, (pad + es_part.get_width() + arrow.get_width(), y))
        y += line_h
    if not words_to_show:
        msg = font_w.render("Visita zonas y recoge palabras para desbloquear el diccionario.", 1, (150, 145, 180))
        surface.blit(msg, (W // 2 - msg.get_width() // 2, y + 20))
    inst = font_small.render("ESC o ENTER: Volver a pausa", 1, (140, 140, 160))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 36))


def draw_credits(surface, font_large, font_small):
    """Pantalla de créditos: tema máscaras y rostros."""
    from draw_mask import draw_mask_oval
    surface.fill((25, 22, 45))
    W, H = surface.get_width(), surface.get_height()
    mask_r = pygame.Rect(W // 2 - 28, 18, 56, 48)
    draw_mask_oval(surface, mask_r, (200, 180, 240), glow=True, eyes=False)
    t = font_large.render("CRÉDITOS", 1, (255, 220, 120))
    surface.blit(t, (W // 2 - t.get_width() // 2, 42))
    lines = [
        "Maskaria: Guardianes Nasa",
        "Un juego sobre máscaras y poderes. Cada máscara rescatada te da un poder único.",
        "",
        "Equipo:",
        "Juliana Chantre Astudillo",
        "Juan Diego Fernández Paz",
        "Sebastián Vallejo Gilón",
        "William Steven Anacona",
        "",
        "Máscaras: Volar (salto en el aire), Nadar (agua), Ver secretos (ocultos), Abrir puertas.",
        "Rescata máscaras: pisa enemigos o habla con NPCs (E).",
        "",
        "Hecho con Python + Pygame.",
        "Gráficos y sonidos: procedurales / libres.",
        "Música: añade OGG/MP3 en assets/music.",
        "",
        "¡Gracias por jugar! Sigue coleccionando máscaras.",
        "",
        "ESC: Volver al menú",
    ]
    y = 100
    for line in lines:
        txt = font_small.render(line, 1, (200, 190, 220))
        surface.blit(txt, (W // 2 - txt.get_width() // 2, y))
        y += 26
    surface.blit(font_small.render("ESC: Volver al menú", 1, (180, 180, 200)), (W // 2 - 80, H - 40))


def draw_options(surface, font_large, font_small, volume_text):
    """Opciones: tema máscaras visible."""
    from draw_mask import draw_mask_oval
    surface.fill((28, 25, 48))
    W, H = surface.get_width(), surface.get_height()
    mask_r = pygame.Rect(W // 2 - 20, 52, 40, 34)
    draw_mask_oval(surface, mask_r, (180, 160, 220), glow=False, eyes=False)
    t = font_large.render("OPCIONES", 1, (255, 220, 120))
    surface.blit(t, (W // 2 - t.get_width() // 2, 58))
    tema = font_small.render("Tema: máscaras. Cada una te da un poder distinto.", 1, (180, 172, 210))
    surface.blit(tema, (W // 2 - tema.get_width() // 2, 108))
    txt = font_small.render(volume_text, 1, (200, 200, 220))
    surface.blit(txt, (W // 2 - txt.get_width() // 2, 200))
    save_tip = font_small.render("El progreso se guarda al pasar puertas y al elegir Menú principal en pausa.", 1, (160, 158, 190))
    surface.blit(save_tip, (W // 2 - save_tip.get_width() // 2, 250))
    inst = font_small.render("ESC: Volver al menú", 1, (140, 140, 160))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 40))


def draw_level_complete(surface, level_name, font_large, font_small):
    surface.fill((30, 50, 40))
    t = font_large.render("¡Sala completada!", 1, (150, 255, 150))
    n = font_small.render(level_name, 1, (200, 220, 200))
    W, H = surface.get_width(), surface.get_height()
    surface.blit(t, (W // 2 - t.get_width() // 2, H // 3))
    surface.blit(n, (W // 2 - n.get_width() // 2, H // 3 + 50))
    inst = font_small.render("ENTER o ESPACIO: Continuar", 1, (180, 200, 180))
    surface.blit(inst, (W // 2 - inst.get_width() // 2, H - 80))


def draw_game_over(surface, font_large, font_small):
    """Game Over con tema máscaras: las máscaras te esperan."""
    from draw_mask import draw_mask_oval
    W, H = surface.get_width(), surface.get_height()
    for y in range(0, H + 8, 8):
        t = y / H
        c = (int(55 + t * 20), int(28 + t * 15), int(35 + t * 15))
        pygame.draw.rect(surface, c, (0, y, W, 8))
    mask_r = pygame.Rect(W // 2 - 40, H // 2 - 90, 80, 70)
    draw_mask_oval(surface, mask_r, (180, 140, 200), glow=True, eyes=True)
    t = font_large.render("Game Over", 1, (255, 120, 120))
    for dx, dy in [(2, 2)]:
        sh = font_large.render("Game Over", 1, (80, 40, 50))
        surface.blit(sh, (W // 2 - t.get_width() // 2 + dx, H // 2 - 28 + dy))
    surface.blit(t, (W // 2 - t.get_width() // 2, H // 2 - 28))
    sub = font_small.render("Las máscaras te esperan. Reintenta.", 1, (220, 200, 230))
    surface.blit(sub, (W // 2 - sub.get_width() // 2, H // 2 + 18))


def draw_parallax_bg(surface, camera_x, world_width, zone_id, screen_h):
    """Fondo con capas que se mueven a distinta velocidad (parallax)."""
    bg = ((60, 70, 100), (80, 80, 120))
    for z in ZONES:
        if z["id"] == zone_id:
            bg = z["bg"]
            break
    W = surface.get_width()
    # Capa lejana (montañas/silueta)
    for i in range(-1, (W // 80) + 2):
        px = (i * 80 - int(camera_x * 0.2)) % (W + 80) - 40
        h = 120 + int(30 * math.sin(px * 0.02))
        pts = [(px, screen_h), (px + 60, screen_h), (px + 50, screen_h - h), (px + 10, screen_h - h * 0.7)]
        dark = (max(0, bg[0][0] - 50), max(0, bg[0][1] - 40), max(0, bg[0][2] - 30))
        pygame.draw.polygon(surface, dark, pts)
    # Capa media (árboles/rocas)
    for i in range(-1, (W // 50) + 2):
        px = (i * 50 - int(camera_x * 0.5)) % (W + 50) - 25
        h = 60 + int(20 * math.sin(px * 0.03))
        r = pygame.Rect(px, screen_h - h, 24, h)
        mid = (max(0, bg[1][0] - 30), max(0, bg[1][1] - 20), max(0, bg[1][2] - 15))
        pygame.draw.rect(surface, mid, r)
        pygame.draw.rect(surface, (40, 35, 30), r, 1)


def draw_zone_splash(surface, zone_name, alpha, font_large):
    """Nombre de la zona al entrar: máscara arriba, texto abajo (tema máscaras)."""
    from draw_mask import draw_mask_oval
    if alpha <= 0:
        return
    W, H = surface.get_width(), surface.get_height()
    # Máscara destacada arriba
    s = pygame.Surface((100, 90), pygame.SRCALPHA)
    draw_mask_oval(s, pygame.Rect(10, 5, 80, 75), (220, 200, 255), glow=True, eyes=True)
    s.set_alpha(min(alpha, 240))
    surface.blit(s, (W // 2 - 50, H // 2 - 100))
    tema = pygame.font.Font(None, 22).render("Nueva zona — más máscaras te esperan", 1, (180, 170, 210))
    tema.set_alpha(alpha)
    surface.blit(tema, (W // 2 - tema.get_width() // 2, H // 2 - 18))
    text = font_large.render(zone_name.upper(), 1, (255, 255, 255))
    tw, th = text.get_size()
    shadow = font_large.render(zone_name.upper(), 1, (50, 40, 80))
    surface.blit(shadow, (W // 2 - tw // 2 + 3, H // 2 + 8))
    text.set_alpha(alpha)
    surface.blit(text, (W // 2 - tw // 2, H // 2 + 5))


def draw_tutorial_hint(surface, text, font_small):
    """Mensajes de pista en el CENTRO de la pantalla para que se vean bien y no se tapen."""
    W, H = surface.get_width(), surface.get_height()
    pad = 24
    lines = text.split("\n")
    max_w = 0
    surfs = []
    for line in lines:
        s = font_small.render(line, 1, (245, 238, 220))
        surfs.append(s)
        max_w = max(max_w, s.get_width())
    box_h = len(lines) * 24 + pad * 2
    box_w = min(max_w + pad * 2, W - 60)
    box_x = W // 2 - box_w // 2
    box_y = H // 2 - box_h // 2 - 20
    overlay = pygame.Surface((box_w, box_h))
    overlay.set_alpha(235)
    overlay.fill((35, 28, 55))
    surface.blit(overlay, (box_x, box_y))
    pygame.draw.rect(surface, (140, 120, 180), (box_x, box_y, box_w, box_h), 2)
    for i, s in enumerate(surfs):
        surface.blit(s, (W // 2 - s.get_width() // 2, box_y + pad + i * 24))


def _wrap_text(font, text, max_width):
    """Devuelve lista de líneas con word-wrap."""
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if font.size(test)[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_speech_bubble_character(surface, line1_es, line2_nasa, font_small, mouth_open, speaker="player"):
    """Personaje que habla: 'player' = protagonista sin máscara (humano); 'nasa_elder' = guía del pueblo Nasa (indígena)."""
    W, H = surface.get_width(), surface.get_height()
    font_bubble = pygame.font.Font(None, 22)
    pad_bubble = 16
    max_bubble_w = min(420, W - 180)
    char_x, char_y = 72, H // 2 - 20
    head_r = 26
    # Cabeza: protagonista = piel; guía Nasa = tono tierra + vincha (banda)
    if speaker == "nasa_elder":
        color_head = (210, 175, 145)
        color_border = (140, 110, 85)
        color_band = (140, 60, 40)  # vincha roja/tierra
    else:
        color_head = (255, 230, 200)
        color_border = (180, 160, 140)
        color_band = None
    pygame.draw.circle(surface, color_head, (char_x, char_y), head_r)
    pygame.draw.circle(surface, color_border, (char_x, char_y), head_r, 2)
    if speaker == "nasa_elder":
        # Vincha (banda) del guía Nasa sobre la frente
        band_y = char_y - head_r + 4
        pygame.draw.rect(surface, color_band, (char_x - head_r - 2, band_y, head_r * 2 + 4, 10), border_radius=2)
        pygame.draw.rect(surface, (100, 40, 25), (char_x - head_r - 2, band_y, head_r * 2 + 4, 10), 1, border_radius=2)
    eye_y = char_y - 8
    pygame.draw.circle(surface, (40, 30, 20), (char_x - 8, eye_y), 4)
    pygame.draw.circle(surface, (40, 30, 20), (char_x + 8, eye_y), 4)
    mouth_y = char_y + 10
    if mouth_open:
        pygame.draw.arc(surface, (80, 60, 50), (char_x - 10, mouth_y - 6, 20, 14), 0, math.pi, 2)
    else:
        pygame.draw.line(surface, (80, 60, 50), (char_x - 8, mouth_y), (char_x + 8, mouth_y), 2)
    # Nube blanca (bocadillo)
    lines_es = _wrap_text(font_bubble, line1_es, max_bubble_w - pad_bubble * 2)
    lines_nasa = _wrap_text(font_bubble, line2_nasa, max_bubble_w - pad_bubble * 2)
    all_lines = [(l, (50, 45, 55)) for l in lines_es] + [(l, (80, 60, 130)) for l in lines_nasa]
    if not all_lines:
        all_lines = [("...", (80, 80, 80))]
    line_h = 20
    bubble_h = len(all_lines) * line_h + pad_bubble * 2
    bubble_w = pad_bubble * 2 + max(font_bubble.size(l[0])[0] for l in all_lines)
    bubble_w = min(bubble_w, max_bubble_w + pad_bubble * 2)
    bubble_x = char_x + head_r + 20
    bubble_y = char_y - bubble_h // 2
    bubble_y = max(40, min(bubble_y, H - bubble_h - 40))
    # Dibujar nube (rectángulo redondeado + cola)
    rect = pygame.Rect(bubble_x, bubble_y, bubble_w, bubble_h)
    pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=12)
    pygame.draw.rect(surface, (220, 218, 210), rect, 2, border_radius=12)
    tail_pts = [(bubble_x - 4, char_y), (bubble_x + 12, char_y - 12), (bubble_x + 12, char_y + 12)]
    pygame.draw.polygon(surface, (255, 255, 255), tail_pts)
    pygame.draw.polygon(surface, (220, 218, 210), tail_pts, 2)
    # Botones play y pausa (esquina superior derecha del bocadillo) con etiquetas
    btn_size = 26
    pause_rect = pygame.Rect(bubble_x + bubble_w - btn_size * 2 - 14, bubble_y + 6, btn_size, btn_size)
    pygame.draw.rect(surface, (100, 90, 140), pause_rect, border_radius=btn_size // 2)
    pygame.draw.rect(surface, (160, 150, 200), pause_rect, 1, border_radius=btn_size // 2)
    pcx, pcy = pause_rect.centerx, pause_rect.centery
    pygame.draw.rect(surface, (255, 255, 255), (pcx - 5, pcy - 6, 3, 12), border_radius=1)
    pygame.draw.rect(surface, (255, 255, 255), (pcx + 2, pcy - 6, 3, 12), border_radius=1)
    play_rect = pygame.Rect(bubble_x + bubble_w - btn_size - 8, bubble_y + 6, btn_size, btn_size)
    pygame.draw.rect(surface, (100, 90, 140), play_rect, border_radius=btn_size // 2)
    pygame.draw.rect(surface, (160, 150, 200), play_rect, 1, border_radius=btn_size // 2)
    vcx, vcy = play_rect.centerx, play_rect.centery
    pygame.draw.polygon(surface, (255, 255, 255), [(vcx - 5, vcy - 6), (vcx - 5, vcy + 6), (vcx + 6, vcy)])
    lbl = pygame.font.Font(None, 18)
    surface.blit(lbl.render("Pausa", 1, (140, 130, 170)), (pause_rect.centerx - 18, pause_rect.bottom + 1))
    surface.blit(lbl.render("Play", 1, (140, 130, 170)), (play_rect.centerx - 12, play_rect.bottom + 1))
    # Texto en la nube: español arriba, Nasa Yuwe abajo
    ty = bubble_y + pad_bubble
    for line, color in all_lines:
        s = font_bubble.render(line, 1, color)
        surface.blit(s, (bubble_x + pad_bubble, ty))
        ty += line_h
    return play_rect, pause_rect


def draw_world_labels(surface, player_rect, water_sprites, door_sprites, cam_x):
    """Etiquetas en el mundo: Yu' cerca del agua, Yat / SALIDA cerca de puertas (Nasa Yuwe)."""
    font_label = pygame.font.Font(None, 24)
    dist = 90
    W = surface.get_width()
    for w in water_sprites:
        dx = player_rect.centerx - w.rect.centerx
        dy = player_rect.centery - w.rect.centery
        if dx * dx + dy * dy < dist * dist:
            sx = w.rect.x - cam_x + w.rect.w // 2
            sy = w.rect.y - 22
            if 0 <= sx <= W - 40:
                t = font_label.render("Yu' (agua)", 1, (255, 255, 255))
                surface.blit(t, (sx - t.get_width() // 2, sy))
            return
    for d in door_sprites:
        dx = player_rect.centerx - d.rect.centerx
        dy = player_rect.centery - d.rect.centery
        if dx * dx + dy * dy < dist * dist:
            sx = d.rect.x - cam_x + d.rect.w // 2
            sy = d.rect.y - 28
            if 0 <= sx <= W - 60:
                t1 = font_label.render("SALIDA", 1, (255, 255, 200))
                t2 = font_label.render("Yat (casa)", 1, (200, 180, 255))
                surface.blit(t1, (sx - t1.get_width() // 2, sy))
                surface.blit(t2, (sx - t2.get_width() // 2, sy + 18))
            return


# Intro de cada nivel: historia sentida por pantalla — pueblo_1 = protagonista; resto = guía Nasa
LEVEL_INTRO_MESSAGES = {
    "pueblo_1": {"es": "No sé quién fui. Solo sé que desperté aquí, en Nasa yat — la casa del pueblo. Los mayores dicen que la primera máscara me dará un rostro. Ayúdame: pisa al que patrulla y toma su máscara.", "nasa": "Nasa yat = casa del pueblo. Cxwa' = máscara."},
    "pueblo_2": {"es": "Ma'ga pe'te. Soy el guía de este lugar. Delante tienes Yu' — el agua. Sin la máscara del Mar te ahogarás. Habla con el pescador (E); él te la entregará. Así aprenderás a nombrar el agua y a atravesarla.", "nasa": "Yu' = agua. Nada con la máscara."},
    "bosque_1": {"es": "Entras a Kiwe — la tierra, el bosque. Aquí no todo se ve a la primera. Pisa al que lleva la máscara del Ojo: con ella verás lo que está escondido. Las palabras de este lugar también están escondidas hasta que las busques.", "nasa": "Kiwe = tierra, bosque. Ver lo escondido."},
    "bosque_2": {"es": "Kiwe nxuu — el bosque profundo. Hay una puerta cerrada que lleva a la cueva. Solo la máscara del Candado la abre. Consíguela pisando al que la guarda. Cada puerta que abres es un paso más en tu camino.", "nasa": "Kiwe nxuu = bosque profundo. Abrir Yat."},
    "cueva_1": {"es": "The'j — la cueva. Aquí el guardián te espera. Habla con él (E): te dará la Máscara del Salto. Podrás saltar otra vez en el aire cuando todo parezca imposible. En Nasa Yuwe, The'j es refugio y prueba.", "nasa": "The'j = cueva. Salta otra vez."},
    "cueva_2": {"es": "Yat — la casa sagrada. El ermitaño vive aquí. Pulsa E para hablar con él: te dará la Máscara del Rayo. Con Q o SHIFT harás dash — atravesarás el peligro en un instante. Ya casi eres otro.", "nasa": "Yat = casa sagrada. Rayo = dash."},
    "ruinas_1": {"es": "Nasa Kiwe — la tierra Nasa, las ruinas. La velocidad te espera: pisa al que lleva esa máscara. Aquí el mundo acelera y tú debes seguir. Cada máscara que llevas es un pedazo de la historia que estás recuperando.", "nasa": "Nasa Kiwe = tierra nasa. Correr más rápido."},
    "abismo_1": {"es": "Yu' the'j — el abismo de agua. Aquí el miedo y la altura se juntan. El que lleva la máscara del Gigante te dará un salto que parece imposible. Ten cuidado: el agua no perdona. Pero tú ya sabes nadar y ya sabes nombrarla.", "nasa": "Yu' the'j = abismo de agua. Salto grande."},
    "cumbre_1": {"es": "Kiwe u' — la cumbre. Has subido hasta aquí. El guardián te dará la Máscara del Escudo (E): un golpe que la vida te perdonará. Ya no eres quien despertó sin rostro. Ki putxuynha'w es adiós; pero tú no vas a despedirte aún.", "nasa": "Kiwe u' = cumbre. Escudo = un golpe menos."},
    "santuario_final": {"es": "Piyayu' — el santuario final. Todas las máscaras. Todas las palabras. Toca la puerta ¡META! y cruza. Quien entra aquí ya no sale igual: sale como guardián. Gracias por haber caminado esta historia.", "nasa": "Piyayu' = santuario. Ki putxuynha'w."},
}

# Al agarrar cada máscara: nombre y qué hace (español + Nasa Yuwe)
MASK_PICKUP_MESSAGES = {
    "fly": {"es": "Máscara del Viento. Mantén SALTO en el aire para volar.", "nasa": "Cxwa' wala — volar en el aire."},
    "swim": {"es": "Máscara del Mar. Nada en el agua (Yu') sin ahogarte.", "nasa": "Yu' — nadar. No te ahogas."},
    "secrets": {"es": "Máscara del Ojo. Revela plataformas y puertas ocultas.", "nasa": "Ver lo escondido — Kiwe, puertas."},
    "doors": {"es": "Máscara del Candado. Abre puertas selladas con E.", "nasa": "Abrir puertas — Yat cerrada."},
    "double": {"es": "Máscara del Salto. Salta otra vez en el aire.", "nasa": "The'j — salto doble."},
    "dash": {"es": "Máscara del Rayo. Pulsa Q o SHIFT para hacer dash.", "nasa": "Rayo — ir muy rápido (dash)."},
    "speed": {"es": "Máscara del Viento Rápido. Corres más rápido.", "nasa": "Nasa Kiwe — correr más rápido."},
    "strong": {"es": "Máscara del Gigante. Salto más alto y potente.", "nasa": "Salto grande — Kiwe u'."},
    "shield": {"es": "Máscara del Escudo. Un golpe extra por vida.", "nasa": "Te protege un golpe. Escudo."},
    "final": {"es": "Máscara del Santuario. Has completado la colección.", "nasa": "Piyayu' — colección completa."},
}

# Pantalla 0 = intención del juego (que dé ganas de jugar). Pantallas 1-10 = un nivel cada una
STORY_SCREENS = [
    "¿POR QUÉ JUGAR MASKARIA?\n\nEste juego nace de un deseo: que el Nasa Yuwe — la lengua del pueblo Nasa, en Colombia — no se pierda. Cuando una lengua desaparece, se pierde una forma única de nombrar el mundo y de decir quiénes somos. Aquí no solo vas a saltar y a correr: vas a caminar una historia, a llevar máscaras que te transforman y a aprender palabras que alguien, en algún lugar, sigue diciendo. Jugar es también cuidar. ¿Listo para empezar?",
    "NIVEL 1 — NASA YAT (La casa del pueblo)\n\nAlguien despertó aquí sin rostro. Sin historia. Los mayores dicen que la primera máscara le dará un nombre. En cada mundo hay una máscara que rescatar o que te entregan: con ella te transformas. En Nasa yat todo empieza. Pisa al que patrulla y tómale la máscara.",
    "NIVEL 2 — YU' (El agua)\n\nDelante está Yu' — el agua. En este mundo la máscara la tiene el pescador: habla con él (E) y te la dará. Sin ella te ahogas; con ella nadas y aprendes a nombrar. Cada nivel guarda una máscara. Esta es la del Mar.",
    "NIVEL 3 — KIWE (La tierra, el bosque)\n\nKiwe es el bosque. Aquí la máscara la lleva quien patrulla: písalo y tómala. Revela lo oculto — senderos y puertas que solo unos ojos pueden ver. En cada mundo, una máscara. En cada máscara, una transformación.",
    "NIVEL 4 — KIWE NXUU (El bosque profundo)\n\nEn el bosque profundo hay una puerta cerrada. La máscara del Candado la abre: pisa al que la guarda y tómala. Sin esa máscara no hay paso. Con ella, avanzas hacia la cueva.",
    "NIVEL 5 — THE'J (La cueva)\n\nThe'j es refugio y prueba. En este mundo el guardián te da la máscara: habla con él (E). La Máscara del Salto te deja saltar otra vez en el aire cuando todo parece imposible. Cada lugar tiene su máscara. Esta es la del Salto.",
    "NIVEL 6 — YAT (La casa sagrada)\n\nEn el corazón de la cueva está Yat. El ermitaño te entrega la Máscara del Rayo (E): con Q o SHIFT harás dash y atravesarás el peligro. En cada mundo, una máscara. Aquí, la del Rayo.",
    "NIVEL 7 — NASA KIWE (Las ruinas)\n\nNasa Kiwe — las ruinas. Aquí la máscara de la Velocidad la lleva quien patrulla: písalo y tómala. El tiempo pesa; correr salva. En cada mundo hay una máscara. No te vayas sin la tuya.",
    "NIVEL 8 — YU' THE'J (El abismo de agua)\n\nYu' the'j es el abismo. La máscara del Gigante (salto potente) la tiene el enemigo: písalo y tómala. Abajo, el agua no perdona. Arriba, el cielo sigue ahí. Cada mundo, una máscara. Esta te da el salto que parece imposible.",
    "NIVEL 9 — KIWE U' (La cumbre)\n\nKiwe u' — la cumbre. El guardián te da la Máscara del Escudo (E): un golpe que la vida te perdona. Ya casi tienes todas. Ya no eres quien despertó sin rostro. En cada mundo había una máscara. Esta es la del Escudo.",
    "NIVEL 10 — PIYAYU' (El santuario final)\n\nPiyayu' — el santuario final. Aquí está la última máscara: recógela y toca la puerta ¡META! Quien lleva todas las máscaras y todas las palabras ya no sale igual: sale como guardián. Gracias por haber caminado esta historia.",
]

def _gradient_rect(surface, rect, color_top, color_bottom):
    """Rellena rect con gradiente vertical de color_top a color_bottom."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    for i in range(h):
        t = i / max(h - 1, 1)
        c = (
            int(color_top[0] + (color_bottom[0] - color_top[0]) * t),
            int(color_top[1] + (color_bottom[1] - color_top[1]) * t),
            int(color_top[2] + (color_bottom[2] - color_top[2]) * t),
        )
        pygame.draw.line(surface, c, (x, y + i), (x + w, y + i))


def _draw_nasa_corner_motif(surface, x, y, size=24):
    """Motivo decorativo Nasa (rombo/sol) para esquina de ilustración — cultura en todas las pantallas."""
    cx, cy = x + size // 2, y + size // 2
    pts = [(cx, cy - size//2 + 2), (cx + size//2 - 2, cy), (cx, cy + size//2 - 2), (cx - size//2 + 2, cy)]
    # Solo borde (no tapa la ilustración)
    pygame.draw.polygon(surface, (180, 155, 120), pts, 2)
    pygame.draw.circle(surface, (255, 235, 200), (cx, cy), 3)


def _draw_nasa_cultural_band(surface, W, y_top, band_height):
    """Banda cultural Nasa (chumbe/tul): franjas de colores parejas y rombos centrados, sin solapamientos."""
    # Franjas horizontales fijas (5 franjas que reparten bien el alto)
    colors = [(140, 45, 35), (35, 28, 25), (240, 235, 220), (115, 85, 55), (180, 55, 45)]
    n_stripes = len(colors)
    stripe_h = band_height // n_stripes
    remainder = band_height - stripe_h * n_stripes
    yy = y_top
    for i in range(n_stripes):
        h = stripe_h + (1 if i < remainder else 0)
        if h <= 0 or yy >= y_top + band_height:
            break
        pygame.draw.rect(surface, colors[i], (0, yy, W, h))
        yy += h
    # Una sola fila de rombos centrados (motivo tul Nasa), sin solapar
    center_y = y_top + band_height // 2
    step = 20
    half_w = 5
    half_h = 4
    x = step // 2
    while x + half_w * 2 <= W:
        pts = [
            (x + half_w, center_y - half_h),  # arriba
            (x + half_w * 2, center_y),       # derecha
            (x + half_w, center_y + half_h), # abajo
            (x, center_y),                   # izquierda
        ]
        pygame.draw.polygon(surface, (255, 248, 235), pts, 1)
        x += step
    # Líneas de borde nítidas
    pygame.draw.line(surface, (90, 72, 58), (0, y_top), (W, y_top), 2)
    pygame.draw.line(surface, (90, 72, 58), (0, y_top + band_height - 1), (W, y_top + band_height - 1), 2)


def _draw_story_illustration(surface, screen_index, W, H_illus):
    """Ilustraciones por pantalla: profesionales, acordes a la narración y al ambiente de cada nivel. Incluyen cultura Nasa."""
    cx, cy = W // 2, H_illus // 2
    # Marco elegante para todas
    _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (22, 20, 38), (32, 28, 48))
    pygame.draw.rect(surface, (55, 48, 78), (0, 0, W, H_illus), 2)
    pygame.draw.rect(surface, (75, 65, 100), (6, 6, W - 12, H_illus - 12), 1)
    idx = screen_index

    if idx == 0:  # Intro: lengua, historia, máscaras — “Una lengua. Una historia. Tú.”
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (45, 35, 65), (28, 22, 42))
        # Sol/mundo suave al fondo
        for r in range(60, 24, -6):
            shade = (min(255, 80 + r), min(255, 70 + r), min(255, 110 + r))
            pygame.draw.circle(surface, shade, (cx, cy - 10), r)
        # Máscara central estilizada (oval + ojos)
        pygame.draw.ellipse(surface, (220, 200, 255), (cx - 42, cy - 55, 84, 70))
        pygame.draw.ellipse(surface, (255, 245, 255), (cx - 38, cy - 50, 76, 62), 1)
        pygame.draw.ellipse(surface, (40, 35, 55), (cx - 22, cy - 38, 12, 14))
        pygame.draw.ellipse(surface, (40, 35, 55), (cx + 8, cy - 38, 12, 14))
        pygame.draw.ellipse(surface, (255, 252, 255), (cx - 18, cy - 42, 4, 5))
        pygame.draw.ellipse(surface, (255, 252, 255), (cx + 12, cy - 42, 4, 5))
        # Rayos suaves (sin texto encima; el lema va en la zona de texto debajo)
        for i in range(16):
            a = i * math.pi * 2 / 16
            ex = cx + int(90 * math.cos(a))
            ey = cy - 10 + int(50 * math.sin(a))
            pygame.draw.line(surface, (180, 170, 220), (cx, cy - 10), (ex, ey), 2)

    elif idx == 1:  # Nasa yat — casa del pueblo, despertar, primera máscara
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (50, 42, 55), (35, 28, 38))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 + 30, W, H_illus//2), (200, 165, 125), (160, 125, 90))
        # Amanecer: disco naranja suave
        pygame.draw.circle(surface, (255, 200, 140), (W - 90, 55), 45)
        pygame.draw.circle(surface, (255, 235, 200), (W - 90, 55), 35)
        # Casas del pueblo (más detalle y personalidad)
        for i, (x, h, roof_h) in enumerate([(W//10, 62, 28), (W//2 - 42, 78, 32), (W*8//10 - 40, 55, 24)]):
            by = H_illus//2 + 42 - h
            # Pared
            pygame.draw.rect(surface, (215, 185, 150), (x, by + h - 22, 52, 24))
            pygame.draw.rect(surface, (195, 168, 128), (x + 2, by + h - 20, 48, 20), 1)
            # Techo (dos aguas)
            pygame.draw.polygon(surface, (175, 95, 55), [(x, by + h - 22), (x + 26, by + h - 22 - roof_h), (x + 52, by + h - 22)])
            pygame.draw.polygon(surface, (155, 85, 48), [(x, by + h - 22), (x + 26, by + h - 22 - roof_h), (x + 52, by + h - 22)], 1)
            # Ventana
            pygame.draw.rect(surface, (255, 240, 200), (x + 14, by + h - 14, 14, 12))
            pygame.draw.rect(surface, (255, 220, 160), (x + 16, by + h - 12, 10, 8))
            # Luz/antorcha en el techo
            pygame.draw.circle(surface, (255, 230, 140), (x + 24, by + h - 24 - roof_h//2), 6)
            pygame.draw.circle(surface, (255, 255, 220), (x + 24, by + h - 24 - roof_h//2), 3)
        # Camino/suelo con textura
        pygame.draw.ellipse(surface, (230, 215, 195), (cx - 50, H_illus//2 + 28, 100, 28))

    elif idx == 2:  # Yu' — el agua, pescador, máscara del Mar
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (100, 165, 220), (55, 120, 185))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 - 10, W, H_illus//2 + 15), (45, 115, 180), (25, 75, 140))
        # Sol y reflejo
        pygame.draw.circle(surface, (255, 250, 220), (W - 70, 50), 38)
        pygame.draw.circle(surface, (255, 245, 200), (W - 70, 50), 28)
        pygame.draw.ellipse(surface, (200, 230, 255), (cx - 55, H_illus//2 + 5, 110, 45))
        pygame.draw.ellipse(surface, (180, 215, 245), (cx - 48, H_illus//2 + 12, 96, 35))
        # Olas en capas (todas arriba de la banda cultural)
        band_top = H_illus - 28
        for row in range(4):
            base_y = H_illus//2 + 12 + row * 12
            if base_y + 38 > band_top:
                break
            for i in range(12):
                px = (i * 88 - row * 20) % (W + 100) - 50
                pygame.draw.arc(surface, (65, 145, 210), (px, base_y - 12, 120, 50), math.pi * 0.2, math.pi * 0.9, 3)
        # Silueta de barca/pescador (simple)
        pygame.draw.polygon(surface, (60, 45, 35), [(W//4, H_illus//2 + 25), (W//4 + 55, H_illus//2 + 25), (W//4 + 48, H_illus//2 + 38)])
        pygame.draw.arc(surface, (75, 55, 40), (W//4 + 8, H_illus//2 + 8, 35, 35), 0, math.pi, 2)

    elif idx == 3:  # Kiwe — bosque, máscara del Ojo, lo oculto
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (35, 55, 42), (22, 38, 28))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 + 35, W, H_illus//2), (48, 95, 55), (28, 62, 38))
        # Luz filtrada (rayos)
        for i in range(5):
            sx = cx - 120 + i * 55
            pts = [(sx, 0), (sx + 35, H_illus//2 + 20), (sx + 70, 0)]
            s = pygame.Surface((W, H_illus), pygame.SRCALPHA)
            pygame.draw.polygon(s, (50, 90, 60, 18), pts)
            surface.blit(s, (0, 0))
        # Árboles con follaje rico
        for i, (x, th, tw) in enumerate([(W//8, 72, 50), (W//2 - 35, 88, 58), (W*3//4 - 25, 65, 44)]):
            ty = H_illus//2 + 38 - th
            pygame.draw.rect(surface, (88, 62, 42), (x + tw//2 - 6, ty + th - 25, 14, 28))
            for j in range(7):
                bx = x + (j % 3) * (tw//2) - 5
                by = ty + (j // 3) * 32
                pygame.draw.circle(surface, (38, 95, 52), (bx, by), 22)
                pygame.draw.circle(surface, (52, 118, 62), (bx + 4, by - 4), 14)
        # Detalle “ojo”: brillo entre árboles
        pygame.draw.circle(surface, (255, 252, 200), (cx + 45, cy - 15), 12)
        pygame.draw.circle(surface, (240, 235, 180), (cx + 45, cy - 15), 6)

    elif idx == 4:  # Kiwe nxuu — bosque profundo, puerta cerrada, Candado
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (22, 42, 28), (18, 32, 22))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 - 20, W, H_illus//2 + 25), (35, 58, 40), (25, 45, 32))
        # Puerta antigua con marco
        door_x, door_y = cx - 58, H_illus//2 - 70
        pygame.draw.rect(surface, (95, 72, 52), (door_x - 8, door_y - 12, 132, 95), border_radius=4)
        pygame.draw.rect(surface, (75, 55, 38), (door_x, door_y, 116, 78), border_radius=2)
        pygame.draw.rect(surface, (55, 42, 28), (door_x + 42, door_y + 22, 32, 42))
        # Candado destacado
        pygame.draw.rect(surface, (180, 155, 80), (cx - 14, door_y + 28, 28, 22), border_radius=4)
        pygame.draw.rect(surface, (220, 200, 120), (cx - 12, door_y + 30, 24, 18), border_radius=2)
        pygame.draw.arc(surface, (160, 140, 70), (cx - 10, door_y + 18, 20, 18), math.pi, 0, 3)
        # Musgo y enredaderas
        pygame.draw.ellipse(surface, (45, 82, 52), (door_x + 8, door_y + 55, 35, 18))
        pygame.draw.ellipse(surface, (42, 75, 48), (door_x + 78, door_y + 12, 28, 14))
        # Antorcha
        pygame.draw.rect(surface, (80, 58, 40), (door_x - 4, door_y + 25, 8, 35))
        pygame.draw.circle(surface, (255, 200, 100), (door_x, door_y + 18), 10)
        pygame.draw.circle(surface, (255, 240, 180), (door_x, door_y + 18), 5)

    elif idx == 5:  # The'j — cueva, refugio, guardián, Salto (arco sin invadir banda cultural)
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (28, 26, 42), (38, 32, 55))
        # Arco de cueva (oscuro), altura limitada para no solapar banda inferior (y >= H_illus-28)
        arc_top = H_illus//2 - 88
        arc_h = (H_illus - 28) - arc_top - 10  # 10 px de margen sobre la banda
        pygame.draw.ellipse(surface, (22, 20, 35), (cx - 130, arc_top, 260, arc_h))
        pygame.draw.ellipse(surface, (35, 30, 52), (cx - 122, arc_top + 8, 244, arc_h - 16), 2)
        # Estalactitas
        for i in range(8):
            sx = cx - 100 + i * 28
            pygame.draw.polygon(surface, (45, 42, 58), [(sx, H_illus//2 - 72), (sx + 12, H_illus//2 + 15), (sx + 24, H_illus//2 - 72)])
        # Fuego/luz interior (refugio)
        pygame.draw.circle(surface, (255, 220, 160), (cx, H_illus//2 + 18), 32)
        pygame.draw.circle(surface, (255, 200, 130), (cx, H_illus//2 + 18), 24)
        pygame.draw.circle(surface, (255, 245, 210), (cx, H_illus//2 + 18), 12)
        # Resplandor
        for r in range(12):
            a = r * math.pi * 2 / 12
            ex = cx + int(75 * math.cos(a))
            ey = H_illus//2 + 18 + int(45 * math.sin(a))
            pygame.draw.line(surface, (200, 180, 140), (cx, H_illus//2 + 18), (ex, ey), 2)

    elif idx == 6:  # Yat — casa sagrada, ermitaño, Rayo/dash
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (42, 36, 58), (55, 48, 75))
        # Luz dorada desde arriba
        pygame.draw.circle(surface, (255, 235, 180), (cx, 52), 55)
        pygame.draw.circle(surface, (255, 220, 160), (cx, 52), 42)
        for r in range(14):
            a = r * math.pi * 2 / 14
            ex = cx + int(100 * math.cos(a))
            ey = 52 + int(58 * math.sin(a))
            pygame.draw.line(surface, (255, 230, 170), (cx, 52), (ex, ey), 3)
        # Altar / mesa sagrada
        pygame.draw.rect(surface, (140, 108, 72), (cx - 62, H_illus//2 + 18, 124, 42), border_radius=6)
        pygame.draw.rect(surface, (165, 130, 90), (cx - 58, H_illus//2 + 22, 116, 34), border_radius=4)
        pygame.draw.ellipse(surface, (255, 215, 130), (cx - 38, H_illus//2 + 20, 76, 28))
        # Rayo (dash): línea de velocidad
        pygame.draw.line(surface, (255, 248, 200), (cx - 90, cy), (cx + 90, cy), 4)
        pygame.draw.line(surface, (255, 240, 180), (cx - 85, cy - 2), (cx + 85, cy - 2), 2)

    elif idx == 7:  # Nasa Kiwe — ruinas, velocidad
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (65, 55, 58), (48, 42, 45))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 + 20, W, H_illus//2), (115, 92, 78), (88, 70, 60))
        # Cielo ruinas (nublado)
        pygame.draw.ellipse(surface, (90, 85, 95), (cx - 80, 25, 160, 50))
        # Columnas rotas con detalle
        for i, (x, h, cap) in enumerate([(W//6, 82, True), (W//2 - 30, 58, True), (W*5//6 - 38, 70, False)]):
            col_y = H_illus//2 + 25 - h
            pygame.draw.rect(surface, (138, 125, 112), (x, col_y, 28, h))
            pygame.draw.rect(surface, (118, 105, 92), (x + 4, col_y + 8, 20, h - 16), 1)
            if cap:
                pygame.draw.rect(surface, (148, 132, 115), (x - 2, col_y - 6, 32, 10), border_radius=2)
            pygame.draw.ellipse(surface, (55, 78, 52), (x + 4, col_y + 14, 20, 12))
            pygame.draw.ellipse(surface, (50, 70, 48), (x + 10, col_y + 28, 12, 8))
        # Líneas de velocidad (viento)
        for i in range(6):
            lx = 80 + i * 165
            pygame.draw.line(surface, (120, 110, 100), (lx, H_illus//2 - 15), (lx + 70, H_illus//2 + 25), 2)
        pygame.draw.rect(surface, (100, 88, 75), (cx - 70, H_illus//2 + 32, 140, 14), border_radius=2)

    elif idx == 8:  # Yu' the'j — abismo de agua, altura, Gigante
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (25, 35, 65), (18, 25, 52))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 + 10, W, H_illus//2), (20, 45, 95), (12, 28, 70))
        # Estrella/luna
        pygame.draw.circle(surface, (255, 252, 230), (W - 68, 48), 28)
        pygame.draw.circle(surface, (240, 238, 220), (W - 68, 48), 20)
        # Pasillo estrecho (plataforma)
        pygame.draw.rect(surface, (95, 88, 110), (cx - 95, H_illus//2 - 38, 190, 32), border_radius=6)
        pygame.draw.rect(surface, (75, 68, 88), (cx - 90, H_illus//2 - 34, 180, 24), border_radius=4)
        # Agua profunda (ondas), sin invadir banda cultural
        band_top = H_illus - 28
        for row in range(5):
            base_y = H_illus//2 + 35 + row * 18
            if base_y + 35 > band_top:
                break
            for i in range(15):
                px = (i * 70 + row * 15) % (W + 80) - 40
                pygame.draw.arc(surface, (28, 55, 115), (px, base_y - 8, 90, 40), math.pi * 0.15, math.pi * 0.9, 2)
        # Gritos de altura (líneas verticales lejanas)
        pygame.draw.line(surface, (45, 50, 85), (W//4, H_illus//2 - 20), (W//4 + 8, H_illus//2 + 50), 1)
        pygame.draw.line(surface, (45, 50, 85), (W*3//4, H_illus//2 - 25), (W*3//4 - 8, H_illus//2 + 48), 1)

    elif idx == 9:  # Kiwe u' — cumbre, Escudo, triunfo
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (175, 195, 230), (135, 155, 200))
        _gradient_rect(surface, pygame.Rect(0, H_illus//2 + 5, W, H_illus//2), (145, 165, 195), (115, 135, 175))
        # Sol brillante
        pygame.draw.circle(surface, (255, 250, 220), (W - 72, 55), 36)
        pygame.draw.circle(surface, (255, 245, 200), (W - 72, 55), 26)
        # Picos nevados (terminan arriba de la banda cultural, no solapan texto)
        band_top = H_illus - 30
        pygame.draw.polygon(surface, (255, 252, 255), [(0, band_top), (W//5, H_illus//2 + 25), (W//2 - 20, H_illus//2 + 50), (W//2 + 20, H_illus//2 + 35), (W*4//5, H_illus//2 + 15), (W, band_top)])
        pygame.draw.polygon(surface, (230, 235, 245), [(0, band_top), (W//5, H_illus//2 + 25), (W//2 - 20, H_illus//2 + 50), (W//2 + 20, H_illus//2 + 35), (W*4//5, H_illus//2 + 15), (W, band_top)], 1)
        pygame.draw.polygon(surface, (200, 210, 225), [(cx - 45, H_illus//2 + 48), (cx, H_illus//2 - 15), (cx + 55, H_illus//2 + 42)])
        pygame.draw.polygon(surface, (255, 253, 255), [(cx - 38, H_illus//2 + 38), (cx, H_illus//2 + 5), (cx + 42, H_illus//2 + 35)])
        # Nube suave
        pygame.draw.ellipse(surface, (250, 248, 255), (cx - 60, 35, 100, 35))
        pygame.draw.ellipse(surface, (240, 238, 250), (cx - 50, 42, 80, 28))

    else:  # 10 — Piyayu' santuario final, todas las máscaras, guardián
        _gradient_rect(surface, pygame.Rect(0, 0, W, H_illus), (55, 45, 85), (42, 35, 68))
        # Sol/máscara dorada central
        pygame.draw.circle(surface, (255, 228, 160), (cx, cy - 10), 58)
        pygame.draw.circle(surface, (255, 215, 140), (cx, cy - 10), 48)
        for r in range(20):
            a = r * math.pi * 2 / 20
            ex = cx + int(95 * math.cos(a))
            ey = cy - 10 + int(65 * math.sin(a))
            pygame.draw.line(surface, (255, 235, 175), (cx, cy - 10), (ex, ey), 3)
        # Máscara ceremonial (oval + ojos)
        pygame.draw.ellipse(surface, (90, 62, 42), (cx - 28, cy - 42, 56, 42))
        pygame.draw.ellipse(surface, (110, 78, 55), (cx - 25, cy - 38, 50, 36), 1)
        pygame.draw.ellipse(surface, (35, 28, 22), (cx - 18, cy - 32, 14, 16))
        pygame.draw.ellipse(surface, (35, 28, 22), (cx + 2, cy - 32, 14, 16))
        pygame.draw.ellipse(surface, (255, 250, 245), (cx - 14, cy - 35, 5, 6))
        pygame.draw.ellipse(surface, (255, 250, 245), (cx + 6, cy - 35, 5, 6))
        # Decoración tipo plumas/rayos laterales
        for side in (-1, 1):
            for i in range(4):
                sx = cx + side * (55 + i * 25)
                pygame.draw.line(surface, (255, 220, 150), (cx + side * 45, cy - 12), (sx, cy - 25 + i * 8), 2)
        # Base sagrada
        pygame.draw.rect(surface, (75, 58, 45), (cx - 70, H_illus//2 + 28, 140, 22), border_radius=6)
        pygame.draw.rect(surface, (95, 75, 55), (cx - 65, H_illus//2 + 32, 130, 14), border_radius=4)

    # Motivo Nasa (rombo/sol) en esquina — cultura visible en cada imagen (la banda va fuera, abajo)
    _draw_nasa_corner_motif(surface, W - 36, 10, 26)


# Narrativa al entrar en cada lugar: incluye nombre en Nasa Yuwe para aprender la lengua
LEVEL_NARRATIVES = {
    "pueblo_1": "Nasa yat — la casa del pueblo. Aquí empieza todo. Tu primera máscara te espera.",
    "pueblo_2": "Yu' — el agua. Sin la máscara del Mar no hay paso. Habla con el pescador (E).",
    "bosque_1": "Kiwe — la tierra, el bosque. Lo que no se ve también existe. Busca la máscara del Ojo.",
    "bosque_2": "Kiwe nxuu — el bosque profundo. La máscara del Candado abre la puerta a la cueva.",
    "cueva_1": "The'j — la cueva. El guardián te dará el Salto (E). The'j es refugio y prueba.",
    "cueva_2": "Yat — la casa sagrada. El ermitaño y la Máscara del Rayo (E). Q o SHIFT = dash.",
    "ruinas_1": "Nasa Kiwe — la tierra Nasa. La velocidad está en quien patrulla. Pisa y toma.",
    "abismo_1": "Yu' the'j — el abismo de agua. La máscara del Gigante te da el salto que necesitas.",
    "cumbre_1": "Kiwe u' — la cumbre. El guardián te dará el Escudo (E). Ya casi eres quien debes ser.",
    "santuario_final": "Piyayu' — el santuario final. Toca la puerta ¡META! y completa el viaje.",
}


def _draw_play_button(surface, x, y, size=36):
    """Dibuja ícono de play (triángulo). Devuelve el rect del botón."""
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, (70, 60, 100), r, border_radius=size // 2)
    pygame.draw.rect(surface, (120, 105, 160), r, 2, border_radius=size // 2)
    cx, cy = r.centerx, r.centery
    # Triángulo play (apuntando a la derecha)
    pts = [(cx - 6, cy - 10), (cx - 6, cy + 10), (cx + 10, cy)]
    pygame.draw.polygon(surface, (255, 255, 255), pts)
    return r


def _draw_pause_button(surface, x, y, size=36):
    """Dibuja ícono de pausa (dos barras). Devuelve el rect del botón."""
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, (70, 60, 100), r, border_radius=size // 2)
    pygame.draw.rect(surface, (120, 105, 160), r, 2, border_radius=size // 2)
    cx, cy = r.centerx, r.centery
    # Dos barras verticales
    bar_w = 5
    gap = 8
    pygame.draw.rect(surface, (255, 255, 255), (cx - gap - bar_w, cy - 10, bar_w, 20), border_radius=2)
    pygame.draw.rect(surface, (255, 255, 255), (cx + gap, cy - 10, bar_w, 20), border_radius=2)
    return r


def draw_story_screen(surface, font_large, font_small, screen_index):
    """Pantalla de historia: ilustración, texto, botón play (escuchar) y pausa. Devuelve (play_rect, pause_rect, texto_para_voz)."""
    surface.fill((22, 18, 35))
    W, H = surface.get_width(), surface.get_height()
    play_rect = None
    pause_rect = None
    text_to_speak = ""
    if screen_index >= len(STORY_SCREENS):
        return play_rect, pause_rect, text_to_speak
    H_illus = 220
    _draw_story_illustration(surface, screen_index, W, H_illus)
    # Banda de colores Nasa justo debajo de la imagen (sobre la línea del borde), sin pisar la ilustración
    _draw_nasa_cultural_band(surface, W, H_illus, 28)
    text_block = STORY_SCREENS[screen_index]
    text_to_speak = text_block.replace("\n\n", " ").replace("\n", " ").strip()
    parts = text_block.split("\n\n", 1)
    title_line = parts[0] if parts else ""
    paragraph = parts[1] if len(parts) > 1 else ""
    # Separación: banda va sobre la línea del borde (H_illus); texto debajo con margen
    band_h = 28
    gap_illus_text = band_h + 24
    pad = 48
    max_w = W - pad * 2
    y = H_illus + gap_illus_text
    # Línea delgada de separación justo debajo de la banda de colores
    sep_y = H_illus + band_h + 6
    pygame.draw.line(surface, (55, 48, 72), (pad, sep_y), (W - pad, sep_y), 1)
    font_title = pygame.font.Font(None, 32)
    font_subtitle = pygame.font.Font(None, 26)
    font_body = pygame.font.Font(None, 24)
    # Pantalla 0: subtítulo "Una lengua. Una historia. Tú." en zona de texto (no sobre la imagen)
    if screen_index == 0:
        sub = font_subtitle.render("Una lengua. Una historia. Tú.", 1, (255, 248, 240))
        surface.blit(sub, (W // 2 - sub.get_width() // 2, y))
        y += 32
    if title_line:
        t = font_title.render(title_line, 1, (255, 235, 200))
        surface.blit(t, (W // 2 - t.get_width() // 2, y))
        y += 36
    if paragraph:
        words = paragraph.split()
        line = ""
        for w in words:
            test = line + " " + w if line else w
            if font_body.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    s = font_body.render(line, 1, (225, 218, 245))
                    surface.blit(s, (W // 2 - s.get_width() // 2, y))
                    y += 22
                line = w
        if line:
            s = font_body.render(line, 1, (225, 218, 245))
            surface.blit(s, (W // 2 - s.get_width() // 2, y))
            y += 22
    # Botones play (escuchar) y pausa (esquina inferior derecha)
    btn_size = 40
    pause_rect = _draw_pause_button(surface, W - 52 - btn_size - 8, H - 58, btn_size)
    play_rect = _draw_play_button(surface, W - 52, H - 58, btn_size)
    play_label = font_small.render("Play", 1, (180, 170, 210))
    surface.blit(play_label, (play_rect.centerx - play_label.get_width() // 2, play_rect.bottom + 2))
    pause_label = font_small.render("Pausa", 1, (180, 170, 210))
    surface.blit(pause_label, (pause_rect.centerx - pause_label.get_width() // 2, pause_rect.bottom + 2))
    hint = font_small.render("ESPACIO o ENTER para continuar  —  " + str(screen_index + 1) + " / " + str(len(STORY_SCREENS)), 1, (150, 140, 180))
    surface.blit(hint, (W // 2 - hint.get_width() // 2, H - 50))
    return play_rect, pause_rect, text_to_speak


def draw_victory_screen(surface, font_large, font_small, masks_count, coins_count, lives_count):
    """Pantalla de victoria: ¡Ganaste! / Guardianes Nasa, narrativa final, estadísticas."""
    surface.fill((30, 45, 60))
    W, H = surface.get_width(), surface.get_height()
    title = font_large.render("¡GANASTE!", 1, (255, 220, 100))
    surface.blit(title, (W // 2 - title.get_width() // 2, H // 6 - 20))
    sub = font_small.render("Completaste el viaje.", 1, (220, 210, 255))
    surface.blit(sub, (W // 2 - sub.get_width() // 2, H // 6 + 22))
    ending = (
        "Ya no eres quien despertó sin rostro. Llevas todas las máscaras y todas las palabras. "
        "Eres guardián Nasa. El Nasa Yuwe — la lengua del pueblo Nasa, en Colombia — sigue vivo "
        "en quien la nombra. Gracias por haberlo nombrado con nosotros. Ki putxuynha'w. Hasta siempre."
    )
    pad, max_w = 24, W - 80
    font = pygame.font.Font(None, 24)
    words = ending.split()
    lines, line = [], ""
    for w in words:
        test = line + " " + w if line else w
        if font.size(test)[0] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    y = H // 4 + 20
    for ln in lines:
        s = font.render(ln, 1, (240, 230, 255))
        surface.blit(s, (W // 2 - s.get_width() // 2, y))
        y += 22
    y += 20
    m = font_small.render("Máscaras reunidas: " + str(masks_count) + " / 10", 1, (255, 255, 255))
    surface.blit(m, (W // 2 - m.get_width() // 2, y))
    c = font_small.render("Monedas: " + str(coins_count), 1, (255, 230, 120))
    surface.blit(c, (W // 2 - c.get_width() // 2, y + 26))
    l = font_small.render("Vidas restantes: " + str(lives_count), 1, (255, 150, 150))
    surface.blit(l, (W // 2 - l.get_width() // 2, y + 52))
    hint = font_small.render("ENTER o ESPACIO: Volver al menú", 1, (180, 170, 210))
    surface.blit(hint, (W // 2 - hint.get_width() // 2, H - 70))
