# Maskaria: Guardianes Nasa - Configuración
# Metroidvania ligero: máscaras de animales, poderes y lengua Nasa Yuwe

TITLE = "Maskaria: Guardianes Nasa"
VERSION = "1.0"

# Pantalla
SCREEN_W = 1024
SCREEN_H = 576
FPS = 60
TILE_SIZE = 32

# HUD: barra superior (el juego se dibuja debajo)
HUD_PANEL_H = 64
HUD_LEFT_W = 280   # Máscara activa
HUD_CENTER_W = 360 # Nombre de sala
# Zona derecha = resto (monedas, vidas, 10 slots de máscaras)

# Física
GRAVITY = 0.5
MAX_FALL = 10
WATER_GRAVITY = 0.15
WATER_MAX_FALL = 3
FLY_LIFT = 0.35
FLY_MAX_UP = -8
SWIM_SPEED_UP = -5
SWIM_SPEED_DOWN = 4

# Juice: coyote time (frames para saltar tras salir de plataforma) y jump buffer
COYOTE_TIME = 8
JUMP_BUFFER = 10

# Cámara: suavizado y deadzone (píxeles desde el centro antes de mover cámara)
CAMERA_SMOOTH = 0.12
CAMERA_DEADZONE_X = 140
CAMERA_DEADZONE_LEFT = 0.35   # ratio de pantalla a la izq del centro
CAMERA_DEADZONE_RIGHT = 0.35  # ratio a la der

# Máscaras (poderes que rescatas) — 10 niveles, 10 máscaras
MASK_FLY = "fly"               # Nivel 1: Volar
MASK_SWIM = "swim"             # Nivel 2: Nadar
MASK_SECRETS = "secrets"       # Nivel 3: Ver secretos
MASK_DOORS = "doors"           # Nivel 4: Abrir puertas
MASK_DOUBLE_JUMP = "double"    # Nivel 5: Doble salto
MASK_DASH = "dash"             # Nivel 6: Dash
MASK_SPEED = "speed"           # Nivel 7: Velocidad
MASK_STRONG = "strong"         # Nivel 8: Salto potente
MASK_SHIELD = "shield"         # Nivel 9: Escudo (una vez por vida)
MASK_FINAL = "final"           # Nivel 10: Máscara final (completar colección)

# Sin máscara especial al inicio
DEFAULT_MASK = None

# Colores por máscara
MASK_COLORS = {
    MASK_FLY: (100, 200, 255),
    MASK_SWIM: (60, 180, 220),
    MASK_SECRETS: (200, 100, 255),
    MASK_DOORS: (255, 180, 80),
    MASK_DOUBLE_JUMP: (180, 120, 255),
    MASK_DASH: (255, 100, 150),
    MASK_SPEED: (100, 255, 150),
    MASK_STRONG: (255, 140, 60),
    MASK_SHIELD: (100, 200, 255),
    MASK_FINAL: (255, 220, 100),
}

# Zonas del mundo: cada nivel tiene su escenario y color distinto; nombre en Nasa Yuwe para enseñar la lengua
ZONES = [
    {"id": "pueblo_inicio", "name": "Pueblo - Inicio", "name_nasa_yuwe": "Nasa yat", "bg": ((255, 235, 200), (220, 170, 120))},
    {"id": "pueblo_laguna", "name": "Pueblo - Laguna", "name_nasa_yuwe": "Yu'", "bg": ((140, 200, 220), (80, 160, 190))},
    {"id": "bosque_entrada", "name": "Bosque - Entrada", "name_nasa_yuwe": "Kiwe", "bg": ((90, 160, 100), (50, 110, 60))},
    {"id": "bosque_profundidad", "name": "Bosque - Profundidad", "name_nasa_yuwe": "Kiwe nxuu", "bg": ((45, 95, 55), (25, 60, 35))},
    {"id": "cueva_entrada", "name": "Cueva - Entrada", "name_nasa_yuwe": "The'j", "bg": ((55, 45, 75), (35, 28, 50))},
    {"id": "cueva_santuario", "name": "Cueva - Santuario", "name_nasa_yuwe": "Yat", "bg": ((120, 90, 70), (180, 140, 80))},
    {"id": "ruinas", "name": "Ruinas", "name_nasa_yuwe": "Nasa Kiwe", "bg": ((130, 85, 65), (90, 55, 45))},
    {"id": "abismo", "name": "Abismo", "name_nasa_yuwe": "Yu' the'j", "bg": ((35, 45, 85), (20, 25, 55))},
    {"id": "cumbre", "name": "Cumbre", "name_nasa_yuwe": "Kiwe u'", "bg": ((180, 195, 220), (120, 145, 185))},
    {"id": "santuario", "name": "Santuario Final", "name_nasa_yuwe": "Piyayu'", "bg": ((90, 75, 130), (255, 215, 110))},
]

# Primera sala al empezar / cargar
START_ROOM_ID = "pueblo_1"

# Zone splash: segundos que se muestra el nombre de zona al entrar
ZONE_SPLASH_DURATION = 2.5

# Puntuación y vidas
COINS_PER_EXTRA_LIFE = 100
INITIAL_LIVES = 3
INITIAL_COINS = 0

# Rutas
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
NASA_YUWE_SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds", "nasa_yuwe")
SAVE_PATH = os.path.join(BASE_DIR, "savegame.json")
