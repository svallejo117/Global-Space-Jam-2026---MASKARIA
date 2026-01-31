# MASKARIA - Mapa del mundo (Overworld) como en Secret Maryo Chronicles
# Nodos por reino, rutas entre niveles, selección con flechas o ratón

import pygame
from config import SCREEN_W, SCREEN_H, REALMS, FINAL_LEVEL_ID, MASK_COLORS, MASK_JUMP, MASK_SPEED, MASK_STRENGTH, MASK_SPECIAL


def get_all_level_ids():
    ids = []
    for realm in REALMS:
        ids.extend(realm["levels"])
    ids.append(FINAL_LEVEL_ID)
    return ids


def build_overworld_nodes():
    """Construye la lista de nodos: (x, y, level_id, realm_name, mask_id, radius)."""
    level_ids = get_all_level_ids()
    nodes = []
    margin = 80
    w, h = SCREEN_W - 2 * margin, SCREEN_H - 2 * margin
    n = len(level_ids)
    if n <= 0:
        return nodes, level_ids
    # Distribuir nodos: 4 reinos en filas, luego nodo final centrado abajo
    realm_colors = {
        MASK_JUMP: MASK_COLORS[MASK_JUMP],
        MASK_SPEED: MASK_COLORS[MASK_SPEED],
        MASK_STRENGTH: MASK_COLORS[MASK_STRENGTH],
        MASK_SPECIAL: MASK_COLORS[MASK_SPECIAL],
    }
    idx = 0
    for ri, realm in enumerate(REALMS):
        realm_name = realm["name"]
        mask_id = realm["mask"]
        level_list = realm["levels"]
        row_y = margin + 120 + ri * 100
        for li, lid in enumerate(level_list):
            col_x = margin + 120 + li * (w - 200) // max(1, len(level_list) - 1) if len(level_list) > 1 else margin + w // 2
            nodes.append({
                "x": col_x, "y": row_y, "level_id": lid,
                "realm": realm_name, "mask": mask_id,
                "radius": 28, "index": idx,
            })
            idx += 1
    # Nodo final
    nodes.append({
        "x": SCREEN_W // 2, "y": SCREEN_H - 100,
        "level_id": FINAL_LEVEL_ID, "realm": "Santuario Final",
        "mask": None, "radius": 36, "index": idx,
    })
    return nodes, level_ids


def draw_overworld(surface, nodes, level_ids, current_index, unlocked_indices, font_title, font_small):
    """Dibuja el mapa del mundo con nodos, rutas y selección."""
    # Fondo gradiente (cielo máscaras)
    for y in range(0, SCREEN_H, 4):
        t = y / SCREEN_H
        c = (
            int(40 + t * 30),
            int(35 + t * 25),
            int(70 + t * 40),
        )
        pygame.draw.rect(surface, c, (0, y, SCREEN_W, 4))
    # Título
    title = font_title.render("MAPA DE LOS REINOS", 1, (255, 240, 200))
    surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 24))
    sub = font_small.render("Selecciona un nivel con las flechas y ENTER. ESC: Menú", 1, (200, 190, 180))
    surface.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 52))

    # Rutas entre nodos consecutivos del mismo reino
    for i, node in enumerate(nodes):
        if i + 1 < len(nodes) and nodes[i + 1]["realm"] == node["realm"]:
            pygame.draw.line(surface, (100, 90, 120), (node["x"], node["y"]), (nodes[i + 1]["x"], nodes[i + 1]["y"]), 4)
    # Ruta al nodo final desde el último de espíritu
    if len(nodes) >= 2:
        last_before_final = nodes[-2]
        final_node = nodes[-1]
        pygame.draw.line(surface, (120, 100, 140), (last_before_final["x"], last_before_final["y"]), (final_node["x"], final_node["y"]), 5)

    # Nodos
    for i, node in enumerate(nodes):
        x, y = node["x"], node["y"]
        r = node["radius"]
        unlocked = node["index"] in unlocked_indices
        is_current = node["index"] == current_index
        if unlocked:
            color = MASK_COLORS.get(node["mask"], (150, 150, 180))
        else:
            color = (80, 75, 90)
        pygame.draw.circle(surface, color, (x, y), r)
        pygame.draw.circle(surface, (60, 55, 70), (x, y), r, 3)
        if is_current:
            pygame.draw.circle(surface, (255, 255, 255), (x, y), r + 4, 4)
        num = font_small.render(str(node["index"] + 1), 1, (255, 255, 255))
        surface.blit(num, (x - num.get_width() // 2, y - num.get_height() // 2))
        if node["realm"] == "Santuario Final":
            lbl = font_small.render("FINAL", 1, (255, 255, 200))
            surface.blit(lbl, (x - lbl.get_width() // 2, y + r + 4))


def get_node_at_mouse(nodes, mx, my):
    """Devuelve el índice del nodo bajo el ratón, o None."""
    for node in nodes:
        dx = mx - node["x"]
        dy = my - node["y"]
        if dx * dx + dy * dy <= node["radius"] * node["radius"]:
            return node["index"]
    return None
