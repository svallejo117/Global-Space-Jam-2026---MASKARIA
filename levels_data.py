# Maskaria: Guardianes Nasa - Salas del mundo (metroidvania)
# #=suelo  X=plataforma oculta  W=agua  S=pinchos  F=plataforma que cae  H/V=obstáculos móviles
# N=enemigo (suelta máscara)  U=momia  K=cangrejo  C=moneda  P=inicio  M=máscara flotante
# Puertas y NPCs en room_data: doors, npcs, enemy_masks

from config import TILE_SIZE, START_ROOM_ID
from masks import (
    MASK_FLY, MASK_SWIM, MASK_SECRETS, MASK_DOORS,
    MASK_DOUBLE_JUMP, MASK_DASH, MASK_SPEED, MASK_STRONG, MASK_SHIELD, MASK_FINAL,
)


def _empty_grid(w, h):
    return [[" " for _ in range(w)] for _ in range(h)]


def _fill_floor(g, row):
    for x in range(len(g[0])):
        g[row][x] = "#"
    return g


ROOMS = {}

# --- PUEBLO 1: inicio, sin máscara. Enemigo con máscara Volar. Momias y pinchos. Puerta a pueblo_2 ---
def _pueblo_1():
    g = _empty_grid(45, 16)
    _fill_floor(g, 15)
    for x in range(45):
        g[15][x] = "#"
    g[14][2] = "P"
    for i in [6, 12, 18, 24]:
        g[14][i] = "#"
    g[13][28] = "#"
    g[14][30] = "U"   # momia
    g[14][32] = "#"
    g[14][34] = "U"   # momia
    g[14][36] = "#"
    g[14][40] = "N"   # enemigo: suelta máscara Volar
    g[14][42] = "#"
    g[14][43] = "#"
    g[14][44] = "#"
    for i in [8, 16, 22]:
        g[14][i] = "C"
    g[13][20] = "S"
    g[13][21] = "S"
    g[13][26] = "S"
    g[13][38] = "S"
    return g


ROOMS["pueblo_1"] = {
    "id": "pueblo_1",
    "zone": "pueblo_inicio",
    "zone_name": "Pueblo - Inicio",
    "grid": _pueblo_1(),
    "doors": [
        {"x": 43, "y": 13, "w": 1, "h": 2, "target": "pueblo_2", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {(40, 14): MASK_FLY},
    "npcs": [],
    "word_pickups": [
        {"x": 8, "y": 13, "word_id": "nasa"},
        {"x": 16, "y": 13, "word_id": "mishi"},
    ],
}

# --- PUEBLO 2: ya tienes Volar. Agua abajo; cangrejos y pinchos. NPC da máscara Nadar. Puerta a bosque_1 ---
def _pueblo_2():
    g = _empty_grid(50, 18)
    for x in range(50):
        g[17][x] = "#"
    for y in range(14, 18):
        for x in range(50):
            if y == 17:
                g[y][x] = "#"
            elif y in (15, 16):
                g[y][x] = "W"
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "K"   # cangrejo
    g[14][10] = "#"
    g[13][14] = "#"
    g[14][18] = "#"
    g[14][20] = "K"
    g[14][22] = "#"
    g[14][26] = "#"
    g[14][30] = "#"
    g[14][34] = "#"
    g[14][36] = "K"
    g[14][38] = "#"
    g[14][42] = "#"
    g[14][44] = "K"
    g[14][46] = "#"
    g[14][48] = "#"
    g[14][49] = "#"
    g[14][24] = "#"
    g[13][12] = "S"
    g[13][13] = "S"
    g[13][20] = "C"
    g[13][32] = "C"
    g[13][40] = "C"
    return g


ROOMS["pueblo_2"] = {
    "id": "pueblo_2",
    "zone": "pueblo_laguna",
    "zone_name": "Pueblo - Laguna",
    "grid": _pueblo_2(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "pueblo_1", "spawn_x": 42 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 48, "y": 13, "w": 1, "h": 2, "target": "bosque_1", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {},
    "npcs": [
        {"x": 24, "y": 13, "mask_id": MASK_SWIM, "message": "Ma'ga pe'te (hola en Nasa Yuwe). Soy el pescador. Toma la Máscara del Mar. Yu' es agua."},
    ],
    "word_pickups": [
        {"x": 10, "y": 13, "word_id": "yu"},
        {"x": 20, "y": 13, "word_id": "magapete"},
    ],
}

# --- BOSQUE 1 (nivel 3): enemigo Ver secretos. Momias, pinchos, obstáculo móvil. Plataformas ocultas. Puerta a bosque_2 ---
def _bosque_1():
    g = _empty_grid(52, 16)
    _fill_floor(g, 15)
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "U"
    g[14][10] = "#"
    g[14][14] = "#"
    g[14][18] = "N"
    g[14][20] = "#"
    g[14][24] = "#"
    g[13][28] = "X"
    g[13][29] = "X"
    g[14][32] = "#"
    g[14][34] = "U"
    g[14][36] = "#"
    g[13][40] = "X"
    g[14][44] = "#"
    g[14][46] = "U"
    g[14][48] = "#"
    g[14][49] = "#"
    g[14][50] = "#"
    g[13][12] = "S"
    g[13][13] = "S"
    g[13][16] = "S"
    g[13][22] = "C"
    g[13][26] = "S"
    g[13][34] = "C"
    g[13][38] = "S"
    g[12][22] = "H"   # obstáculo móvil horizontal (evitar)
    return g


ROOMS["bosque_1"] = {
    "id": "bosque_1",
    "zone": "bosque_entrada",
    "zone_name": "Bosque - Entrada",
    "grid": _bosque_1(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "pueblo_2", "spawn_x": 47 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 50, "y": 13, "w": 1, "h": 2, "target": "bosque_2", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {(18, 14): MASK_SECRETS},
    "npcs": [],
}

# --- BOSQUE 2: puerta cerrada. Enemigo máscara Abrir puertas. Momias, pinchos, plataforma que cae. ---
def _bosque_2():
    g = _empty_grid(48, 16)
    _fill_floor(g, 15)
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][10] = "#"
    g[14][12] = "U"
    g[14][14] = "#"
    g[14][18] = "#"
    g[14][22] = "N"
    g[14][24] = "#"
    g[14][26] = "U"
    g[14][30] = "#"
    g[14][34] = "#"
    g[14][38] = "F"   # plataforma que cae
    g[14][39] = "F"
    g[14][42] = "#"
    g[14][44] = "#"
    g[14][45] = "#"
    g[14][46] = "#"
    g[13][8] = "S"
    g[13][9] = "S"
    g[13][24] = "C"
    g[13][28] = "S"
    g[13][36] = "C"
    g[13][40] = "S"
    return g


ROOMS["bosque_2"] = {
    "id": "bosque_2",
    "zone": "bosque_profundidad",
    "zone_name": "Bosque - Profundidad",
    "grid": _bosque_2(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "bosque_1", "spawn_x": 47 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 46, "y": 13, "w": 1, "h": 2, "target": "cueva_1", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": True},
    ],
    "enemy_masks": {(22, 14): MASK_DOORS},
    "npcs": [],
}

# --- CUEVA 1: agua, pinchos, momias y obstáculo vertical. Nadar y Ver secretos. Puerta a cueva_2 ---
def _cueva_1():
    g = _empty_grid(50, 18)
    for x in range(50):
        g[17][x] = "#"
    for y in range(14, 17):
        for x in range(20, 35):
            g[y][x] = "W"
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "U"
    g[14][10] = "#"
    g[14][18] = "#"
    g[14][21] = "#"
    g[14][24] = "#"
    g[13][22] = "X"
    g[13][23] = "X"
    g[14][26] = "#"
    g[14][28] = "U"
    g[14][32] = "#"
    g[14][36] = "#"
    g[14][38] = "U"
    g[14][40] = "#"
    g[14][44] = "#"
    g[14][47] = "#"
    g[14][48] = "#"
    g[13][12] = "S"
    g[13][13] = "S"
    g[13][28] = "S"
    g[13][29] = "S"
    g[13][32] = "C"
    g[13][40] = "S"
    g[12][30] = "V"
    return g


ROOMS["cueva_1"] = {
    "id": "cueva_1",
    "zone": "cueva_entrada",
    "zone_name": "Cueva - Entrada (Nivel 5)",
    "grid": _cueva_1(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "bosque_2", "spawn_x": 45 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 48, "y": 13, "w": 1, "h": 2, "target": "cueva_2", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {},
    "npcs": [
        {"x": 32, "y": 13, "mask_id": MASK_DOUBLE_JUMP, "message": "Ma'ga pe'te. Soy el guardián. The'j es cueva en Nasa Yuwe. Toma la Máscara del Salto: podrás saltar otra vez en el aire."},
    ],
}

# --- CUEVA 2: santuario. Momias, pinchos y obstáculo móvil. NPC Máscara Rayo. ---
def _cueva_2():
    g = _empty_grid(40, 16)
    _fill_floor(g, 15)
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "U"
    g[14][10] = "#"
    g[14][14] = "#"
    g[14][18] = "#"
    g[14][20] = "#"
    g[14][22] = "#"
    g[14][24] = "#"
    g[14][26] = "#"
    g[14][28] = "#"
    g[14][30] = "#"
    g[14][32] = "U"
    g[14][34] = "#"
    g[14][38] = "#"
    g[13][12] = "S"
    g[13][20] = "C"
    g[13][28] = "C"
    g[13][34] = "S"
    g[12][16] = "H"
    return g


ROOMS["cueva_2"] = {
    "id": "cueva_2",
    "zone": "cueva_santuario",
    "zone_name": "Cueva - Santuario (Nivel 6)",
    "grid": _cueva_2(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "cueva_1", "spawn_x": 47 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 38, "y": 13, "w": 1, "h": 2, "target": "ruinas_1", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {},
    "npcs": [
        {"x": 20, "y": 13, "mask_id": MASK_DASH, "message": "Ma'ga pe'te. Yat es casa sagrada en Nasa Yuwe. Soy el ermitaño. Toma la Máscara del Rayo: pulsa Q o SHIFT para hacer dash."},
    ],
}

# Orden de niveles (1 a 10) y sala final para victoria
LEVEL_ORDER = [
    "pueblo_1", "pueblo_2", "bosque_1", "bosque_2", "cueva_1", "cueva_2",
    "ruinas_1", "abismo_1", "cumbre_1", "santuario_final"
]
FINAL_ROOM_ID = "santuario_final"  # Al salir por la puerta final → victoria

# --- NIVEL 7: Ruinas. Enemigo Velocidad. Momias, cangrejos, pinchos, obstáculos, plataforma que cae. Puerta a abismo_1 ---
def _ruinas_1():
    g = _empty_grid(45, 18)
    for x in range(45):
        g[17][x] = "#"
    for y in range(15, 17):
        for x in range(20, 40):
            g[y][x] = "W"
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "U"
    g[14][10] = "#"
    g[13][14] = "S"
    g[13][15] = "S"
    g[14][18] = "#"
    g[14][20] = "K"
    g[14][22] = "#"
    g[14][26] = "N"
    g[14][28] = "#"
    g[14][30] = "U"
    g[14][34] = "#"
    g[14][36] = "F"
    g[14][37] = "F"
    g[14][38] = "#"
    g[14][42] = "#"
    g[14][43] = "#"
    g[14][44] = "#"
    g[13][20] = "#"
    g[13][24] = "#"
    g[13][28] = "S"
    g[13][32] = "C"
    g[13][36] = "C"
    g[13][40] = "S"
    g[12][16] = "H"
    g[12][32] = "V"
    return g

ROOMS["ruinas_1"] = {
    "id": "ruinas_1",
    "zone": "ruinas",
    "zone_name": "Ruinas - Nivel 7",
    "grid": _ruinas_1(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "cueva_2", "spawn_x": 37 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 43, "y": 13, "w": 1, "h": 2, "target": "abismo_1", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {(26, 14): MASK_SPEED},
    "npcs": [],
}

# --- NIVEL 8: Abismo. Enemigo máscara Gigante (salto potente). Agua, cangrejos, pinchos, obstáculos. Puerta a cumbre_1 ---
def _abismo_1():
    g = _empty_grid(50, 18)
    for x in range(50):
        g[17][x] = "#"
    for y in range(14, 17):
        for x in range(15, 38):
            g[y][x] = "W"
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "K"
    g[14][10] = "#"
    g[14][12] = "#"
    g[14][14] = "#"
    g[14][18] = "#"
    g[14][20] = "K"
    g[14][22] = "#"
    g[14][26] = "N"   # enemigo MASK_STRONG (Gigante)
    g[14][28] = "#"
    g[14][30] = "#"
    g[14][32] = "#"
    g[14][34] = "#"
    g[14][36] = "K"
    g[14][38] = "#"
    g[14][42] = "#"
    g[14][44] = "K"
    g[14][46] = "#"
    g[14][48] = "#"
    g[14][49] = "#"
    g[13][16] = "S"
    g[13][17] = "S"
    g[13][20] = "S"
    g[13][21] = "S"
    g[13][28] = "C"
    g[13][34] = "S"
    g[13][40] = "C"
    g[12][24] = "V"
    g[12][38] = "H"
    return g

ROOMS["abismo_1"] = {
    "id": "abismo_1",
    "zone": "abismo",
    "zone_name": "Abismo - Nivel 8",
    "grid": _abismo_1(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "ruinas_1", "spawn_x": 42 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 48, "y": 13, "w": 1, "h": 2, "target": "cumbre_1", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {(26, 14): MASK_STRONG},
    "npcs": [],
}

# --- NIVEL 9: Cumbre. Momias, pinchos, obstáculos, plataforma que cae. NPC Escudo. Puerta a santuario_final ---
def _cumbre_1():
    g = _empty_grid(48, 18)
    for x in range(48):
        g[17][x] = "#"
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[13][10] = "#"
    g[14][12] = "U"
    g[14][14] = "#"
    g[13][18] = "S"
    g[13][19] = "S"
    g[14][22] = "#"
    g[14][24] = "U"
    g[14][26] = "#"
    g[14][28] = "#"
    g[13][30] = "#"
    g[14][32] = "F"
    g[14][33] = "F"
    g[14][34] = "#"
    g[14][38] = "#"
    g[14][40] = "U"
    g[14][42] = "#"
    g[14][45] = "#"
    g[14][46] = "#"
    g[14][47] = "#"
    g[13][14] = "S"
    g[13][24] = "C"
    g[13][36] = "C"
    g[12][20] = "H"
    g[12][36] = "V"
    return g

ROOMS["cumbre_1"] = {
    "id": "cumbre_1",
    "zone": "cumbre",
    "zone_name": "Cumbre - Nivel 9",
    "grid": _cumbre_1(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "abismo_1", "spawn_x": 45 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 46, "y": 13, "w": 1, "h": 2, "target": "santuario_final", "spawn_x": 64, "spawn_y": 14 * TILE_SIZE, "locked": False},
    ],
    "enemy_masks": {},
    "npcs": [
        {"x": 28, "y": 13, "mask_id": MASK_SHIELD, "message": "Ma'ga pe'te. Kiwe u' es la cumbre en Nasa Yuwe. Toma la Máscara del Escudo: te protege de un golpe por vida. Ki putxuynha'w cuando partas (adiós)."},
    ],
}

# --- NIVEL 10: Santuario final. Momias y cangrejos como último desafío, pinchos, obstáculo. Salida victoria ---
def _santuario_final():
    g = _empty_grid(42, 16)
    _fill_floor(g, 15)
    g[14][0] = "#"
    g[14][1] = "#"
    g[14][2] = "P"
    g[14][6] = "#"
    g[14][8] = "U"
    g[14][10] = "#"
    g[14][14] = "#"
    g[14][16] = "K"
    g[14][18] = "#"
    g[14][20] = "#"   # plataforma bajo la máscara final
    g[13][20] = "M"   # máscara final (recoger para completar)
    g[14][22] = "#"
    g[14][24] = "U"
    g[14][26] = "#"
    g[14][28] = "K"
    g[14][30] = "#"
    g[14][34] = "#"
    g[14][36] = "U"
    g[14][38] = "#"
    g[14][40] = "#"
    g[14][41] = "#"
    g[13][10] = "S"
    g[13][11] = "S"
    g[13][12] = "C"
    g[13][20] = "S"
    g[13][28] = "C"
    g[13][34] = "S"
    g[12][20] = "H"
    return g

ROOMS["santuario_final"] = {
    "id": "santuario_final",
    "zone": "santuario",
    "zone_name": "Santuario Final - Nivel 10",
    "grid": _santuario_final(),
    "doors": [
        {"x": 0, "y": 13, "w": 1, "h": 2, "target": "cumbre_1", "spawn_x": 45 * TILE_SIZE, "spawn_y": 14 * TILE_SIZE, "locked": False},
        {"x": 40, "y": 13, "w": 1, "h": 2, "target": "victory", "spawn_x": 0, "spawn_y": 0, "locked": False},
    ],
    "enemy_masks": {},
    "npcs": [],
    "mask_pickup_at": {(20, 13): MASK_FINAL},
}


def get_room(room_id):
    return ROOMS.get(room_id)


def get_start_room_id():
    return START_ROOM_ID


def get_all_room_ids():
    return list(ROOMS.keys())
