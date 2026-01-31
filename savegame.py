# Maskaria: Guardianes Nasa - Guardado (sala, posición, máscaras, vidas, monedas)

import json
import os
from config import SAVE_PATH, INITIAL_LIVES, INITIAL_COINS, START_ROOM_ID, TILE_SIZE


def load():
    default = {
        "room_id": START_ROOM_ID,
        "player_x": 64,
        "player_y": 12 * TILE_SIZE,  # rect.y para pies sobre plataforma (fila 14)
        "collected_masks": [],
        "current_mask": None,
        "lives": INITIAL_LIVES,
        "coins": INITIAL_COINS,
        "total_score": 0,
        "game_completed": False,
        "levels_visited": [],
        "glossary_unlocked": [],
        "words_collected": [],
    }
    if not os.path.isfile(SAVE_PATH):
        return default
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in default.items():
            if k not in data:
                data[k] = v
        return data
    except Exception:
        return default


def save(data):
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def save_state(room_id, player_x, player_y, collected_masks, current_mask, lives, coins, game_completed=False):
    data = load()
    data["room_id"] = room_id
    data["player_x"] = player_x
    data["player_y"] = player_y
    data["collected_masks"] = list(collected_masks) if collected_masks else []
    data["current_mask"] = current_mask
    data["lives"] = lives
    data["coins"] = coins
    if game_completed:
        data["game_completed"] = True
    if room_id and room_id not in data.get("levels_visited", []):
        visited = data.get("levels_visited", [])
        visited.append(room_id)
        data["levels_visited"] = visited
    save(data)


def add_coins(amount):
    data = load()
    data["coins"] = data.get("coins", 0) + amount
    extra_lives = 0
    while data["coins"] >= 100:
        data["coins"] -= 100
        data["lives"] = data.get("lives", INITIAL_LIVES) + 1
        extra_lives += 1
    save(data)
    return data["coins"], extra_lives


def set_lives(lives):
    data = load()
    data["lives"] = lives
    save(data)


def get_lives():
    return load().get("lives", INITIAL_LIVES)


def get_coins():
    return load().get("coins", INITIAL_COINS)


def get_glossary_unlocked():
    return list(load().get("glossary_unlocked", []))


def add_glossary_word(word_id):
    data = load()
    lst = data.get("glossary_unlocked", [])
    if word_id not in lst:
        lst.append(word_id)
        data["glossary_unlocked"] = lst
        save(data)


def get_words_collected():
    return list(load().get("words_collected", []))


def add_word_collected(word_id):
    data = load()
    lst = data.get("words_collected", [])
    if word_id not in lst:
        lst.append(word_id)
        data["words_collected"] = lst
        data["glossary_unlocked"] = list(set(data.get("glossary_unlocked", []) + [word_id]))
        save(data)
