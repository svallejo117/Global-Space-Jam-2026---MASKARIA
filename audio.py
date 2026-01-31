# MASKARIA - Audio (recursos libres / placeholders)
# Sonidos procedurales agradables; música y SFX reemplazables por archivos libres

import os
import math
import struct
import pygame
from config import SOUNDS_DIR, MUSIC_DIR, NASA_YUWE_SOUNDS_DIR

_initialized = False
_ambient_channel = None
_ambient_sound = None

SAMPLE_RATE = 22050


def init_audio():
    global _initialized
    if _initialized:
        return
    try:
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        _initialized = True
    except Exception:
        pass


def _tone(freq, duration_sec, volume=0.35, attack=0.02, decay=0.1):
    """Genera un tono con envolvente suave (attack/decay) para que no suene duro."""
    n = int(round(duration_sec * SAMPLE_RATE))
    buf = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = 1.0
        if attack > 0 and t < attack:
            env = t / attack
        elif decay > 0 and t > duration_sec - decay:
            env = (duration_sec - t) / decay
        val = int(32767 * volume * env * (0.5 + 0.5 * math.sin(2 * math.pi * freq * t)))
        buf.append(struct.pack("<h", max(-32768, min(32767, val))))
    return b"".join(buf)


def _soft_thud(duration_sec=0.12, base_freq=90, volume=0.25):
    """Sonido suave de aterrizaje: bajo con decay rápido, tipo 'pof'."""
    n = int(round(duration_sec * SAMPLE_RATE))
    buf = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 25)  # decay rápido
        val = int(32767 * volume * env * (0.5 + 0.5 * math.sin(2 * math.pi * base_freq * t * (1 - t * 2))))
        buf.append(struct.pack("<h", max(-32768, min(32767, val))))
    return b"".join(buf)


def play_mask_pickup():
    """Sonido al obtener una máscara: nota brillante y suave."""
    try:
        buf = _tone(523, 0.08, 0.3) + _tone(659, 0.1, 0.25, attack=0.01, decay=0.06)
        s = pygame.mixer.Sound(buffer=buf)
        s.play()
    except Exception:
        pass


def play_jump():
    try:
        s = pygame.mixer.Sound(buffer=_tone(392, 0.06, 0.28, attack=0.01, decay=0.03))
        s.play()
    except Exception:
        pass


def play_level_complete():
    try:
        buf = _tone(523, 0.1, 0.3) + _tone(659, 0.1, 0.28) + _tone(784, 0.15, 0.25, decay=0.08)
        s = pygame.mixer.Sound(buffer=buf)
        s.play()
    except Exception:
        pass


def play_door_open():
    """Sonido al abrir puerta o cambiar de sala."""
    try:
        s = pygame.mixer.Sound(buffer=_tone(330, 0.1, 0.28, attack=0.02, decay=0.06))
        s.play()
    except Exception:
        pass


def play_stomp():
    """Sonido al pisar enemigo: bajo y corto."""
    try:
        s = pygame.mixer.Sound(buffer=_tone(180, 0.08, 0.3, attack=0.01, decay=0.05))
        s.play()
    except Exception:
        pass


def play_land():
    """Sonido al aterrizar: suave y agradable, no un beep feo."""
    try:
        s = pygame.mixer.Sound(buffer=_soft_thud(0.14, 85, 0.22))
        s.play()
    except Exception:
        pass


def play_coin():
    """Sonido al recoger moneda."""
    try:
        s = pygame.mixer.Sound(buffer=_tone(880, 0.06, 0.28, attack=0.01, decay=0.04))
        s.play()
    except Exception:
        pass


def play_hurt():
    """Sonido al recibir daño: bajo y breve."""
    try:
        s = pygame.mixer.Sound(buffer=_tone(150, 0.1, 0.32, attack=0.005, decay=0.07))
        s.play()
    except Exception:
        pass


def play_word_sound(word_id):
    """Reproduce pronunciación en Nasa Yuwe si existe assets/sounds/nasa_yuwe/{word_id}.wav"""
    try:
        if not word_id:
            return
        path = os.path.join(NASA_YUWE_SOUNDS_DIR, str(word_id) + ".wav")
        if os.path.isfile(path):
            s = pygame.mixer.Sound(path)
            s.play()
    except Exception:
        pass


def play_music(loop=True):
    """Reproduce música de fondo si existe en assets/music."""
    try:
        if os.path.isdir(MUSIC_DIR):
            for f in os.listdir(MUSIC_DIR):
                if f.endswith((".ogg", ".mp3", ".wav")):
                    path = os.path.join(MUSIC_DIR, f)
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play(-1 if loop else 0)
                    return
    except Exception:
        pass


# --- Ambientes procedurales (gratuitos, medieval tranquilo / juego) ---

def _generate_ambient_story(seconds=6.0):
    """Fondo medieval tranquilo: drones en quintas/cuartas, modal. Buffer estéreo para mixer (channels=2)."""
    n = int(round(seconds * SAMPLE_RATE))
    buf = []
    for i in range(n):
        t = i / SAMPLE_RATE
        f1, f2 = 73, 110
        f3 = 146 * (0.6 + 0.15 * math.sin(t * 0.25))
        vol = 0.28
        env = 0.5 + 0.25 * math.sin(t * 0.2) + 0.15 * math.sin(t * 0.45)
        s1 = math.sin(2 * math.pi * f1 * t) * 0.55
        s2 = math.sin(2 * math.pi * f2 * t) * 0.3
        s3 = math.sin(2 * math.pi * f3 * t) * 0.18
        val = max(-32768, min(32767, int(32767 * vol * env * (s1 + s2 + s3))))
        sample = struct.pack("<h", val)
        buf.append(sample)
        buf.append(sample)
    return b"".join(buf)


def _generate_ambient_game(seconds=5.0):
    """Ambiente sutil durante el juego: bajo continuo suave, algo de movimiento."""
    n = int(round(seconds * SAMPLE_RATE))
    buf = []
    for i in range(n):
        t = i / SAMPLE_RATE
        f1 = 82
        f2 = 98 + 4 * math.sin(t * 0.4)
        vol = 0.08
        env = 0.5 + 0.3 * math.sin(t * 0.2)
        s1 = math.sin(2 * math.pi * f1 * t) * 0.6
        s2 = math.sin(2 * math.pi * f2 * t) * 0.25
        val = int(32767 * vol * env * (s1 + s2))
        buf.append(struct.pack("<h", max(-32768, min(32767, val))))
    return b"".join(buf)


def stop_ambient():
    """Detiene el ambiente procedural que esté sonando."""
    global _ambient_channel, _ambient_sound
    try:
        if _ambient_channel is not None and _ambient_channel.get_busy():
            _ambient_channel.fadeout(400)
        _ambient_channel = None
        _ambient_sound = None
    except Exception:
        pass


def play_ambient_story():
    """Reproduce fondo medieval tranquilo para pantallas de historia (gratuito, procedural)."""
    global _ambient_channel, _ambient_sound
    stop_ambient()
    try:
        buf = _generate_ambient_story(6.0)
        _ambient_sound = pygame.mixer.Sound(buffer=buf)
        _ambient_channel = _ambient_sound.play(loops=-1)
        if _ambient_channel is not None:
            _ambient_channel.set_volume(0.7)
    except Exception:
        pass


def play_ambient_game():
    """Reproduce ambiente sutil durante el juego (bajo, acorde al nivel)."""
    global _ambient_channel, _ambient_sound
    stop_ambient()
    try:
        buf = _generate_ambient_game(5.0)
        _ambient_sound = pygame.mixer.Sound(buffer=buf)
        _ambient_channel = _ambient_sound.play(loops=-1)
        if _ambient_channel is not None:
            _ambient_channel.set_volume(0.4)
    except Exception:
        pass
