# MASKARIA: El Legado de las Máscaras

## Resumen del proyecto

**MASKARIA** es un juego de plataformas 2D original con temática de **máscaras legendarias** y reinos. El proyecto se inspiró en la mecánica clásica de plataformas (como Secret Maryo Chronicles / SMC) pero es **totalmente original** en narrativa, arte y diseño.

- **Motor:** Python 3 + Pygame  
- **Plataforma:** Windows (ejecutable .exe generado con PyInstaller)  
- **Sin referencias** a Mario, Nintendo ni a SMC en el contenido jugable.

---

## Cambios y características implementadas

### 1. Narrativa
- **Mundo dividido en reinos:** cada reino representa una máscara legendaria.
- **Cuatro reinos:** Reino del Salto, Reino de la Velocidad, Reino de la Fuerza, Reino del Espíritu.
- **Santuario Final:** nivel de desafío final que reúne todas las máscaras.

### 2. Sistema de máscaras (gameplay) — poderes reales
- **Máscaras intercambiables:** al recoger una máscara en el nivel, el personaje cambia de poder.
- **Poderes por máscara:**
  - **Máscara del Salto:** doble salto en el aire (salto extra para alcanzar plataformas altas).
  - **Máscara de la Velocidad:** dash supersónico (S) para atravesar pinchos y obstáculos.
  - **Máscara de la Fuerza:** rompe bloques marrones (B) y golpe al suelo (ABAJO en el aire) para romper desde arriba.
  - **Máscara del Espíritu:** fase fantasmal (S): invencibilidad breve y atraviesa pinchos sin daño.
- **UI clara:** barra superior muestra la máscara activa, descripción del poder, reino/nivel, vidas y barra de especial.
- **Efecto visual** al cambiar de máscara (resplandor y partículas).
- **Trampas y dificultad:** pinchos (S), plataformas que caen (F), obstáculos móviles (H/V), bloques rompibles (B).

### 3. Visual
- Estilo **colorido e intuitivo**: cada máscara tiene un color distintivo (jugador, HUD, recogibles).
- **Arte procedural:** plataformas y niveles generados por código (sin sprites externos de SMC).
- Efectos al **cambiar de máscara** y al usar la habilidad especial.

### 4. Audio
- **Sonidos generados por código** como fallback (tonos al saltar, al recoger máscara, al completar nivel).
- Se pueden **reemplazar por recursos libres**: colocar archivos en `assets/sounds/` y `assets/music/` (ogg, mp3, wav) y el juego los usará si están disponibles.

### 5. Niveles
- Niveles **re-tematizados por reino/máscara** (Reino del Salto, Velocidad, Fuerza, Espíritu).
- **Un nivel final de desafío** (Santuario Final) con varias máscaras y mayor longitud.

### 6. Controles
- **Flechas o A/D:** mover.
- **Espacio:** salto (doble salto con Máscara del Salto).
- **ABAJO (flecha abajo):** golpe al suelo con Máscara de la Fuerza (rompe bloques desde arriba).
- **S:** habilidad especial: dash (Velocidad) o fase fantasmal (Espíritu).
- **ESC:** pausa / volver al menú.

---

## Cómo ejecutar el juego (desarrollo)

1. **Requisitos:** Python 3.8+ y Pygame.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar:
   ```bash
   python main.py
   ```
   (Desde la carpeta `MASKARIA`.)

---

## Cómo volver a compilar el ejecutable (.exe) para Windows

1. Instalar PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Desde la carpeta del proyecto (`MASKARIA`):
   ```bash
   pyinstaller build.spec
   ```
3. El ejecutable se generará en:
   ```
   dist/MASKARIA.exe
   ```
4. Opcional: incluir la carpeta `assets` (música/sonidos propios) junto al .exe o empaquetarla; el `build.spec` ya incluye `assets` si existe.

---

## Estructura del proyecto

```
MASKARIA/
├── main.py           # Bucle principal, estados (título, juego, nivel completo, game over)
├── config.py         # Constantes, título, máscaras, reinos
├── masks.py          # Poderes por máscara (salto, velocidad, fuerza, especial)
├── player.py         # Jugador, física, cambio de máscara, habilidad especial
├── levels_data.py    # Datos de niveles por reino + nivel final
├── world.py          # Plataformas, bloques rompibles, recogibles de máscara, salida
├── ui.py             # HUD (máscara activa, vidas, pantallas de título y fin)
├── audio.py          # Sonidos y música (placeholders + soporte archivos libres)
├── effects.py        # Sacudida de cámara y partículas (máscara, bloque roto, daño)
├── requirements.txt  # pygame
├── build.spec        # PyInstaller para generar MASKARIA.exe
├── DOCUMENTACION.md  # Este archivo
└── assets/
    ├── sounds/       # Opcional: sonidos .ogg/.wav
    └── music/        # Opcional: música .ogg/.mp3/.wav
```

---

## Nota sobre SMC (Secret Maryo Chronicles)

El código fuente de **MASKARIA** está escrito desde cero en Python/Pygame. No se modificó el código C++ de SMC; se utilizó solo como referencia de género (plataformas 2D). Si se desea adaptar el proyecto original de SMC (C++, SDL, CEGUI) con la misma temática de máscaras, haría falta:

- Renombrar referencias "Maryo" → personaje portador de máscaras.
- Sustituir tipos de power-up por "máscaras" y ajustar lógica de poderes.
- Cambiar textos, assets y nombre del proyecto a "MASKARIA" en el código y en los instaladores (NSIS, etc.).

Para una entrega jugable en Windows sin depender de la cadena de compilación de SMC, esta versión en Pygame permite jugar de inmediato y generar un .exe con PyInstaller.
