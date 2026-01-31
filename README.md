# Maskaria: Guardianes Nasa

Metroidvania ligero 2D: exploras un mundo con **máscaras de animales** que rescatas de enemigos o recibes de NPCs. Cada máscara te transforma en ese animal y te da un **poder** (volar, nadar, ver secretos, abrir puertas). Aprende palabras en **Nasa Yuwe**, la lengua del pueblo Nasa. Algunas zonas solo se abren con la máscara correcta.

## Cómo jugar
- **A / D** o **Flechas**: mover
- **ESPACIO / ARRIBA**: salto
- **E**: interactuar (hablar con NPCs, abrir puertas cerradas si tienes la máscara)
- **Máscara Volar**: mantén **SALTO** en el aire para volar
- **Máscara Nadar**: atraviesa agua sin ahogarte
- **Máscara Ver secretos**: revela plataformas y puertas ocultas
- **Máscara Abrir puertas**: permite abrir puertas selladas (E junto a la puerta)
- **ESC**: pausa

## Progresión
1. **Pueblo 1**: Pisa al enemigo para rescatar la **Máscara del Viento** (volar). Llega a la puerta derecha.
2. **Pueblo 2**: Hay agua; sin máscara Nadar ahogas. Habla con el **pescador (E)** para obtener la **Máscara del Mar** (nadar). Sigue a la derecha al Bosque.
3. **Bosque 1**: Pisa al enemigo para rescatar la **Máscara del Ojo** (ver secretos). Aparecen plataformas ocultas. Avanza al Bosque 2.
4. **Bosque 2**: Pisa al enemigo para rescatar la **Máscara del Candado** (abrir puertas). La puerta a la Cueva está cerrada: acércate y pulsa **E** con esa máscara.
5. **Cueva 1 y 2**: Agua y plataformas ocultas. Llega al santuario.

## Requisitos
- Python 3.8+
- Pygame: `pip install pygame`
- **Voz (opcional):** para que el juego lea en voz alta la historia y los textos del guía Nasa, instala `pyttsx3`: `pip install pyttsx3`. En las pantallas de historia y en el bocadillo del personaje hay un botón de altavoz (o tecla **V**) para escuchar el texto.

## Ejecutar
```bash
cd MASKARIA
python main.py
```

## Música y sonidos
El juego usa tonos procedurales por defecto. Para música real: coloca archivos **OGG** o **MP3** en `assets/music/` (uno cualquiera se reproducirá en bucle). Ver `ASSETS_LIBRE.md` para enlaces a recursos libres.

## Nasa Yuwe (lengua del pueblo Nasa, Colombia)
El juego incluye un **diccionario jugable** en Nasa Yuwe: en **Pausa → Palabras en Nasa Yuwe** verás las palabras desbloqueadas con formato **Español → Nasa Yuwe**. Las palabras se desbloquean al visitar cada zona y al recoger **palabras coleccionables** (objetos con "?" en el nivel). Para **pronunciación**: coloca archivos **WAV** en `assets/sounds/nasa_yuwe/` con el nombre del id de la palabra (ej. `yu.wav`, `mishi.wav`, `magapete.wav`). Al recoger esa palabra se reproducirá el audio si el archivo existe.

## Guardado
El progreso (sala actual, posición, máscaras, vidas, monedas) se guarda en `savegame.json` al cambiar de sala o al salir (si implementas guardado al salir).

## Licencia
Código y diseño: uso libre. Assets externos según sus propias licencias (ver ASSETS_LIBRE.md).
