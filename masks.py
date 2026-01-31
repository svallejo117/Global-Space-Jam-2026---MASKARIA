# Maskaria: Guardianes Nasa - Sistema de máscaras (10 niveles, 10 poderes)

from config import (
    MASK_FLY, MASK_SWIM, MASK_SECRETS, MASK_DOORS,
    MASK_DOUBLE_JUMP, MASK_DASH, MASK_SPEED, MASK_STRONG, MASK_SHIELD, MASK_FINAL,
    MASK_COLORS, TILE_SIZE
)

# Nombre en Nasa Yuwe y animal que presenta la máscara (Ma'ga pe'te, yo soy X)
MASK_NASA_ANIMAL = {
    MASK_FLY: {"nasa": "Cxwa' wala", "animal": "Mishi", "animal_es": "gato"},
    MASK_SWIM: {"nasa": "Yu'", "animal": "Wayra", "animal_es": "pez"},
    MASK_SECRETS: {"nasa": "Ver lo escondido", "animal": "Kwe'sx", "animal_es": "ave"},
    MASK_DOORS: {"nasa": "Abrir Yat", "animal": "Tëj", "animal_es": "guardían"},
    MASK_DOUBLE_JUMP: {"nasa": "The'j salto", "animal": "Sëkx", "animal_es": "sapo"},
    MASK_DASH: {"nasa": "Rayo", "animal": "Kwsx", "animal_es": "rayo"},
    MASK_SPEED: {"nasa": "Nasa Kiwe", "animal": "We'sx", "animal_es": "venado"},
    MASK_STRONG: {"nasa": "Kiwe u'", "animal": "Yu'j", "animal_es": "oso"},
    MASK_SHIELD: {"nasa": "Escudo", "animal": "Tëj", "animal_es": "guardían"},
    MASK_FINAL: {"nasa": "Piyayu'", "animal": "Mayor", "animal_es": "sabio"},
}

MASK_STATS = {
    MASK_FLY: {
        "name": "Máscara del Viento",
        "desc": "Mantén SALTO en el aire para volar",
        "fly": True, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": False, "speed": False, "strong": False, "shield": False,
        "jump_power": 12.0, "move_speed": 4.0,
    },
    MASK_SWIM: {
        "name": "Máscara del Mar",
        "desc": "Nada en el agua sin ahogarte",
        "fly": False, "swim": True, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": False, "speed": False, "strong": False, "shield": False,
        "jump_power": 11.0, "move_speed": 4.0,
    },
    MASK_SECRETS: {
        "name": "Máscara del Ojo",
        "desc": "Revela plataformas y puertas ocultas",
        "fly": False, "swim": False, "see_secrets": True, "open_doors": False,
        "double_jump": False, "dash": False, "speed": False, "strong": False, "shield": False,
        "jump_power": 11.0, "move_speed": 4.2,
    },
    MASK_DOORS: {
        "name": "Máscara del Candado",
        "desc": "Abre puertas selladas (E junto a la puerta)",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": True,
        "double_jump": False, "dash": False, "speed": False, "strong": False, "shield": False,
        "jump_power": 11.0, "move_speed": 4.0,
    },
    MASK_DOUBLE_JUMP: {
        "name": "Máscara del Salto",
        "desc": "Salta otra vez en el aire (SALTO en el aire)",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": True, "dash": False, "speed": False, "strong": False, "shield": False,
        "jump_power": 10.5, "move_speed": 4.0,
    },
    MASK_DASH: {
        "name": "Máscara del Rayo",
        "desc": "Dash horizontal (Q o SHIFT)",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": True, "speed": False, "strong": False, "shield": False,
        "jump_power": 11.0, "move_speed": 4.0,
    },
    MASK_SPEED: {
        "name": "Máscara del Viento Rápido",
        "desc": "Corre más rápido",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": False, "speed": True, "strong": False, "shield": False,
        "jump_power": 11.0, "move_speed": 5.5,
    },
    MASK_STRONG: {
        "name": "Máscara del Gigante",
        "desc": "Salto más alto y potente",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": False, "speed": False, "strong": True, "shield": False,
        "jump_power": 13.0, "move_speed": 4.0,
    },
    MASK_SHIELD: {
        "name": "Máscara del Escudo",
        "desc": "Un golpe extra por vida (te protege una vez)",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": False, "speed": False, "strong": False, "shield": True,
        "jump_power": 11.0, "move_speed": 4.0,
    },
    MASK_FINAL: {
        "name": "Máscara del Santuario",
        "desc": "La máscara final. Has completado la colección.",
        "fly": False, "swim": False, "see_secrets": False, "open_doors": False,
        "double_jump": False, "dash": False, "speed": False, "strong": False, "shield": False,
        "jump_power": 11.0, "move_speed": 4.0,
    },
}


def can_fly(mask_id):
    return MASK_STATS.get(mask_id, {}).get("fly", False)


def can_swim(mask_id):
    return MASK_STATS.get(mask_id, {}).get("swim", False)


def can_see_secrets(mask_id):
    return MASK_STATS.get(mask_id, {}).get("see_secrets", False)


def can_open_doors(mask_id):
    return MASK_STATS.get(mask_id, {}).get("open_doors", False)


def can_double_jump(mask_id):
    return MASK_STATS.get(mask_id, {}).get("double_jump", False)


def can_dash(mask_id):
    return MASK_STATS.get(mask_id, {}).get("dash", False)


def can_speed(mask_id):
    return MASK_STATS.get(mask_id, {}).get("speed", False)


def can_strong(mask_id):
    return MASK_STATS.get(mask_id, {}).get("strong", False)


def can_shield(mask_id):
    return MASK_STATS.get(mask_id, {}).get("shield", False)


def get_jump_power(mask_id):
    return MASK_STATS.get(mask_id, {}).get("jump_power", 11.0)


def get_move_speed(mask_id):
    return MASK_STATS.get(mask_id, {}).get("move_speed", 4.0)


def get_mask_name(mask_id):
    return MASK_STATS.get(mask_id, {}).get("name", "Máscara")


def get_mask_desc(mask_id):
    return MASK_STATS.get(mask_id, {}).get("desc", "")


def get_mask_color(mask_id):
    return MASK_COLORS.get(mask_id, (200, 200, 200))


def get_all_mask_ids():
    return [
        MASK_FLY, MASK_SWIM, MASK_SECRETS, MASK_DOORS,
        MASK_DOUBLE_JUMP, MASK_DASH, MASK_SPEED, MASK_STRONG, MASK_SHIELD, MASK_FINAL
    ]


def get_mask_name_nasa(mask_id):
    return MASK_NASA_ANIMAL.get(mask_id, {}).get("nasa", "")


def get_mask_animal(mask_id):
    return MASK_NASA_ANIMAL.get(mask_id, {}).get("animal", "")


def get_mask_animal_es(mask_id):
    return MASK_NASA_ANIMAL.get(mask_id, {}).get("animal_es", "")
