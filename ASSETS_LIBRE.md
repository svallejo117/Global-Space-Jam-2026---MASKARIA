# Assets libres para Maskaria: Guardianes Nasa

El juego usa gráficos y sonidos procedurales por defecto. Puedes reemplazarlos por assets libres (CC0, CC-BY, etc.) para un aspecto más profesional.

## Música (assets/music/)
- **OpenGameArt**: https://opengameart.org/ (busca "platformer music", "exploration")
- **Freesound**: https://freesound.org/ (música bajo Creative Commons)
- **Kenney**: https://kenney.nl/assets (CC0, packs de música)
- Formato recomendado: **OGG** o **MP3**. Coloca un archivo en `assets/music/` y se reproducirá en bucle.

## Sonidos (assets/sounds/)
- **Freesound**: https://freesound.org/ (salto, moneda, puerta, daño)
- **Kenney**: https://kenney.nl/assets (SFX pack, CC0)
- **OpenGameArt**: efectos cortos
- Nombres sugeridos: `jump.ogg`, `coin.ogg`, `door.ogg`, `hurt.ogg`, `mask.ogg`

## Gráficos / sprites
- **OpenGameArt**: personajes 2D, tiles, enemigos
- **Kenney**: https://kenney.nl/assets (Platformer packs, CC0)
- **itch.io**: muchos packs gratuitos con atribución (CC-BY)
- El juego dibuja todo con formas (rectángulos, círculos); para usar sprites haría falta integrar `pygame.image.load()` en `player.py`, `world.py` y el HUD.

## Fuentes
- **Google Fonts**: muchas bajo Open Font License
- **Kenney Fonts**: https://kenney.nl/assets (CC0)
- El juego usa `pygame.font.Font(None, size)` (fuente por defecto). Para fuentes custom: `pygame.font.Font("ruta/fuente.ttf", size)`.

---
*Maskaria: Guardianes Nasa* — Metroidvania ligero. Motor: Python + Pygame.
