# Maskaria: Guardianes Nasa - Dibujo de máscaras (forma oval, ojos, brillo) y formas de animal
# Una sola función reutilizable para jugador, enemigos, pickups y HUD

import pygame


def _dark(color, d=50):
    return (max(0, color[0] - d), max(0, color[1] - d), max(0, color[2] - d))


def _light(color, d=50):
    return (min(255, color[0] + d), min(255, color[1] + d), min(255, color[2] + d))


def draw_character_as_animal(surface, rect, color, animal_es, facing_right=True, invincible_flash=False):
    """Dibuja al personaje como la forma del animal de la máscara dentro de rect.
    animal_es: 'gato', 'pez', 'ave', 'guardían', 'sapo', 'rayo', 'venado', 'oso', 'sabio'.
    invincible_flash: si True, alternar color a blanco (invencibilidad)."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx, cy = x + w // 2, y + h // 2
    fill = (255, 255, 255) if invincible_flash else color
    dark = _dark(fill)
    light = _light(fill)
    dir_ = 1 if facing_right else -1

    # Normalizar nombre (guardían -> guardian para comparar)
    key = (animal_es or "").strip().lower().replace("í", "i").replace("á", "a")

    if key == "gato":
        # Cuerpo oval, orejas triangulares arriba, cola
        body = pygame.Rect(x + w // 6, y + h // 3, w * 2 // 3, h * 2 // 3)
        pygame.draw.ellipse(surface, fill, body)
        pygame.draw.ellipse(surface, dark, body, 1)
        # Orejas
        ear_w, ear_h = w // 4, h // 4
        pygame.draw.polygon(surface, fill, [
            (x + w // 4 - (0 if facing_right else ear_w // 2), y + h // 4),
            (x + w // 4 + (ear_w // 2 if facing_right else 0), y + h // 4),
            (x + w // 4, y - 2),
        ])
        pygame.draw.polygon(surface, fill, [
            (x + 3 * w // 4 + (0 if facing_right else ear_w // 2), y + h // 4),
            (x + 3 * w // 4 - (ear_w // 2 if facing_right else 0), y + h // 4),
            (x + 3 * w // 4, y - 2),
        ])
        pygame.draw.polygon(surface, dark, [(x + w // 4, y + h // 4), (x + w // 4 + dir_ * 4, y + h // 4), (x + w // 4 + dir_ * 2, y)], 1)
        pygame.draw.polygon(surface, dark, [(x + 3 * w // 4, y + h // 4), (x + 3 * w // 4 - dir_ * 4, y + h // 4), (x + 3 * w // 4 - dir_ * 2, y)], 1)
        # Ojos
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - w // 4 - 2, cy - h // 4 - 2, 4, 5))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx + w // 4 - 2, cy - h // 4 - 2, 4, 5))
        # Cola
        pygame.draw.line(surface, fill, (x + (w if facing_right else 0), cy), (x + (w + dir_ * 12 if facing_right else -dir_ * 12), cy - 4), 3)
        pygame.draw.line(surface, dark, (x + (w if facing_right else 0), cy), (x + (w + dir_ * 12 if facing_right else -dir_ * 12), cy - 4), 1)

    elif key == "pez":
        # Cuerpo alargado (elipse horizontal), aleta dorsal, cola en V (cabeza = lado del ojo, cola = lado opuesto)
        body = pygame.Rect(x + 4, y + h // 4, w - 8, h // 2)
        pygame.draw.ellipse(surface, fill, body)
        pygame.draw.ellipse(surface, dark, body, 1)
        # Cola en el lado contrario a donde mira (facing_right = cabeza a la derecha, cola a la izquierda)
        tail_x = x + (6 if facing_right else w - 6)
        pygame.draw.polygon(surface, fill, [
            (tail_x, cy), (tail_x - dir_ * 14, cy - 8), (tail_x - dir_ * 14, cy + 8),
        ])
        pygame.draw.polygon(surface, dark, [(tail_x, cy), (tail_x - dir_ * 14, cy - 8), (tail_x - dir_ * 14, cy + 8)], 1)
        # Ojo del lado de la cabeza (facing_right = ojo a la derecha)
        eye_x = cx + dir_ * (w // 4)
        pygame.draw.circle(surface, (25, 25, 30), (eye_x, cy - 2), 3)
        # Aleta dorsal
        pygame.draw.polygon(surface, fill, [(cx - 4, y + h // 4), (cx + 4, y + h // 4), (cx, y + 6)])
        pygame.draw.polygon(surface, dark, [(cx - 4, y + h // 4), (cx + 4, y + h // 4), (cx, y + 6)], 1)

    elif key == "ave":
        # Cuerpo redondo, alas (arcos o elipses), pico
        pygame.draw.ellipse(surface, fill, (x + w // 6, y + h // 4, w * 2 // 3, h * 2 // 3))
        pygame.draw.ellipse(surface, dark, (x + w // 6, y + h // 4, w * 2 // 3, h * 2 // 3), 1)
        beak_x = x + (w - 4 if facing_right else 4)
        pygame.draw.polygon(surface, dark, [(beak_x, cy), (beak_x + dir_ * 10, cy - 3), (beak_x + dir_ * 10, cy + 3)])
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - w // 5, cy - h // 5, 4, 5))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx + w // 5 - 4, cy - h // 5, 4, 5))
        # Alas (arcos a los lados)
        wing_y = cy
        wing_r = w // 3
        try:
            pygame.draw.arc(surface, fill, (cx - wing_r - 4, wing_y - wing_r // 2, wing_r * 2, wing_r), 0, 3.14, 2)
            pygame.draw.arc(surface, fill, (cx - wing_r + 4, wing_y - wing_r // 2, wing_r * 2, wing_r), 3.14, 6.28, 2)
        except Exception:
            pass

    elif key == "guardian" or key == "guardían":
        # Guardián: forma de máscara oval con escudo (rectángulo redondeado)
        head = pygame.Rect(x + w // 6, y, w * 2 // 3, h // 2 + 4)
        pygame.draw.ellipse(surface, fill, head)
        pygame.draw.ellipse(surface, dark, head, 1)
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - w // 5, cy - h // 4 - 2, 4, 5))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx + w // 5 - 4, cy - h // 4 - 2, 4, 5))
        body = pygame.Rect(x + w // 4, y + h // 2 - 2, w // 2, h // 2 + 2)
        pygame.draw.rect(surface, fill, body, border_radius=4)
        pygame.draw.rect(surface, dark, body, 1, border_radius=4)

    elif key == "sapo":
        # Cuerpo ancho, ojos grandes arriba, patas cortas
        body = pygame.Rect(x + w // 6, y + h // 3, w * 2 // 3, h * 2 // 3)
        pygame.draw.ellipse(surface, fill, body)
        pygame.draw.ellipse(surface, dark, body, 1)
        pygame.draw.circle(surface, (25, 25, 30), (cx - w // 4, y + h // 3 + 4), 5)
        pygame.draw.circle(surface, (25, 25, 30), (cx + w // 4, y + h // 3 + 4), 5)
        pygame.draw.circle(surface, (255, 255, 255), (cx - w // 4 - 1, y + h // 3 + 2), 1)
        pygame.draw.circle(surface, (255, 255, 255), (cx + w // 4 - 1, y + h // 3 + 2), 1)
        # Patas
        pygame.draw.line(surface, fill, (x + w // 4, y + h - 4), (x + w // 4 - 4, y + h + 2), 2)
        pygame.draw.line(surface, fill, (x + 3 * w // 4, y + h - 4), (x + 3 * w // 4 + 4, y + h + 2), 2)
        pygame.draw.line(surface, dark, (x + w // 4, y + h - 4), (x + w // 4 - 4, y + h + 2), 1)
        pygame.draw.line(surface, dark, (x + 3 * w // 4, y + h - 4), (x + 3 * w // 4 + 4, y + h + 2), 1)

    elif key == "rayo":
        # Forma de rayo: zigzag o diamante angular
        pts = [(cx, y + 4), (x + w - 8, cy - 4), (cx, cy), (x + 8, cy + 4), (cx, y + h - 4)]
        if not facing_right:
            pts = [(x + w - (p[0] - x), p[1]) for p in pts]
        pygame.draw.polygon(surface, fill, pts)
        pygame.draw.polygon(surface, light, pts, 1)
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - 3, cy - 4, 5, 5))

    elif key == "venado":
        # Cuerpo oval, astas ramificadas arriba, cara alargada
        body = pygame.Rect(x + w // 6, y + h // 3, w * 2 // 3, h * 2 // 3)
        pygame.draw.ellipse(surface, fill, body)
        pygame.draw.ellipse(surface, dark, body, 1)
        # Astas (líneas desde arriba de la cabeza)
        pygame.draw.line(surface, dark, (cx - 6, y + h // 5), (cx - 14, y - 2), 2)
        pygame.draw.line(surface, dark, (cx - 6, y + h // 5), (cx - 10, y + 2), 2)
        pygame.draw.line(surface, dark, (cx + 6, y + h // 5), (cx + 14, y - 2), 2)
        pygame.draw.line(surface, dark, (cx + 6, y + h // 5), (cx + 10, y + 2), 2)
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - w // 5, cy - h // 5, 4, 5))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx + w // 5 - 4, cy - h // 5, 4, 5))

    elif key == "oso":
        # Cuerpo redondo grande, orejas redondas, hocico
        body = pygame.Rect(x + 4, y + h // 4, w - 8, h * 3 // 4)
        pygame.draw.ellipse(surface, fill, body)
        pygame.draw.ellipse(surface, dark, body, 1)
        pygame.draw.circle(surface, fill, (x + w // 4, y + h // 5), 6)
        pygame.draw.circle(surface, fill, (x + 3 * w // 4, y + h // 5), 6)
        pygame.draw.circle(surface, dark, (x + w // 4, y + h // 5), 6, 1)
        pygame.draw.circle(surface, dark, (x + 3 * w // 4, y + h // 5), 6, 1)
        snout_x = cx + dir_ * (w // 4)
        pygame.draw.ellipse(surface, dark, (snout_x - 4, cy - 2, 8, 6))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - w // 5, cy - h // 5, 4, 5))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx + w // 5 - 4, cy - h // 5, 4, 5))

    elif key == "sabio":
        # Sabio (búho): cara redonda, ojos grandes, pico pequeño
        pygame.draw.circle(surface, fill, (cx, cy), min(w, h) // 2 - 2)
        pygame.draw.circle(surface, dark, (cx, cy), min(w, h) // 2 - 2, 1)
        pygame.draw.ellipse(surface, (25, 25, 30), (cx - w // 4, cy - h // 6, w // 4, h // 4))
        pygame.draw.ellipse(surface, (25, 25, 30), (cx, cy - h // 6, w // 4, h // 4))
        pygame.draw.polygon(surface, dark, [(cx + dir_ * 4, cy + 4), (cx + dir_ * 12, cy + 2), (cx + dir_ * 12, cy + 6)])
        pygame.draw.circle(surface, (255, 255, 255), (cx - w // 6, cy - 2), 2)
        pygame.draw.circle(surface, (255, 255, 255), (cx + w // 6 - 2, cy - 2), 2)

    else:
        # Fallback: máscara oval (forma humana)
        draw_mask_oval(surface, rect, fill, glow=False, eyes=True)
        return
    return


def draw_title_mask(surface, rect, color, glow=True):
    """Máscara destacada para título/menú: más detalle, estilo ceremonial, brillo fuerte.
    Inspirada en máscaras ceremoniales: ojos expresivos, ceja/banda, detalles dorados."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx, cy = x + w // 2, y + h // 2
    dark = _dark(color, 55)
    light = _light(color, 50)
    gold = (255, 220, 120)
    gold_dark = (180, 150, 50)

    # Halo exterior (más capas y suave)
    if glow:
        for i in range(5):
            ex = 12 + i * 6
            ey = 10 + i * 5
            rr = pygame.Rect(x - ex, y - ey, w + ex * 2, h + ey * 2)
            alpha = max(0, 35 - i * 7)
            try:
                s = pygame.Surface((rr.w, rr.h), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (*light, alpha), (0, 0, rr.w, rr.h))
                surface.blit(s, rr.topleft)
            except TypeError:
                s = pygame.Surface((rr.w, rr.h))
                s.set_alpha(alpha)
                pygame.draw.ellipse(s, light, (0, 0, rr.w, rr.h))
                surface.blit(s, rr.topleft)

    # Borde exterior (dorado suave)
    pygame.draw.ellipse(surface, gold_dark, (x - 2, y - 2, w + 4, h + 4), 2)
    pygame.draw.ellipse(surface, color, (x, y, w, h))
    # Arco de brillo superior
    try:
        pygame.draw.arc(surface, light, (x, y, w, h), 3.2, 6.1, 2)
    except Exception:
        pass

    # Banda/ceja decorativa (arco arriba de los ojos, estilo ceremonial)
    brow_y = cy - h // 3
    pygame.draw.arc(surface, gold_dark, (cx - w // 2 - 4, brow_y - 10, w + 8, 22), 3.14, 0, 2)
    pygame.draw.line(surface, gold, (cx - w // 4, brow_y - 2), (cx + w // 4, brow_y - 2), 1)

    # Ojos más grandes y expresivos (con brillo)
    eye_w, eye_h = max(4, w // 5), max(5, h // 4)
    eye_off_x, eye_off_y = w // 4, h // 5
    for ex in (-1, 1):
        ox = cx + ex * (eye_off_x + eye_w // 2)
        oy = cy - eye_off_y
        pygame.draw.ellipse(surface, (20, 18, 25), (ox - eye_w // 2 - 1, oy - eye_h // 2 - 1, eye_w + 2, eye_h + 2))
        pygame.draw.ellipse(surface, (35, 32, 45), (ox - eye_w // 2, oy - eye_h // 2, eye_w, eye_h))
        pygame.draw.ellipse(surface, (255, 252, 245), (ox - 2, oy - 3, 3, 4))

    # Boca suave (línea curva)
    try:
        pygame.draw.arc(surface, dark, (cx - w // 4, cy, w // 2, h // 3), 0, 3.14, 1)
    except Exception:
        pass

    # Detalles laterales (plumas/líneas decorativas)
    for side in (-1, 1):
        sx = cx + side * (w // 2 + 4)
        for i in range(3):
            sy = cy - 15 + i * 12
            pygame.draw.line(surface, gold_dark, (sx, sy), (sx + side * 10, sy - side * 4), 1)
    # Borde final claro
    pygame.draw.ellipse(surface, light, (x, y, w, h), 1)


def draw_mask_oval(surface, rect, color, glow=False, eyes=True, eye_color=(25, 25, 30)):
    """Dibuja una máscara ovalada dentro de rect. color=tono de la máscara.
    glow=brillo exterior; eyes=ojos (círculos)."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx, cy = x + w // 2, y + h // 2
    # Brillo exterior (halo)
    if glow:
        lighter = (min(255, color[0] + 90), min(255, color[1] + 90), min(255, color[2] + 100))
        for i, (ex, ey) in enumerate([(8, 8), (5, 5), (2, 2)]):
            rr = pygame.Rect(x - ex, y - ey, w + ex * 2, h + ey * 2)
            alpha = max(0, 30 - i * 10)
            try:
                s = pygame.Surface((rr.w, rr.h), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (*lighter, alpha), (0, 0, rr.w, rr.h))
                surface.blit(s, rr.topleft)
            except TypeError:
                s = pygame.Surface((rr.w, rr.h))
                s.set_alpha(alpha)
                pygame.draw.ellipse(s, lighter, (0, 0, rr.w, rr.h))
                surface.blit(s, rr.topleft)
    # Borde oscuro (sombra de la máscara)
    pygame.draw.ellipse(surface, (max(0, color[0] - 60), max(0, color[1] - 50), max(0, color[2] - 40)),
                        (x - 1, y - 1, w + 2, h + 2), 2)
    # Relleno
    pygame.draw.ellipse(surface, color, (x, y, w, h))
    # Línea superior (brillo)
    try:
        pygame.draw.arc(surface, (min(255, color[0] + 60), min(255, color[1] + 50), min(255, color[2] + 40)),
                       (x, y, w, h), 3.14159, 0, 1)
    except Exception:
        pass
    # Ojos
    if eyes and w >= 12 and h >= 10:
        eye_w, eye_h = max(2, w // 6), max(2, h // 5)
        off_x, off_y = w // 4, h // 4
        pygame.draw.ellipse(surface, eye_color, (cx - off_x - eye_w // 2, cy - off_y - eye_h // 2, eye_w, eye_h))
        pygame.draw.ellipse(surface, eye_color, (cx + off_x - eye_w // 2, cy - off_y - eye_h // 2, eye_w, eye_h))
    # Borde final
    pygame.draw.ellipse(surface, (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 50)),
                        (x, y, w, h), 1)
