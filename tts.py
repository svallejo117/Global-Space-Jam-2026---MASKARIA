# Maskaria - Texto a voz (TTS) para historia y bocadillos del guía Nasa
# En Windows usa SAPI por PowerShell si pyttsx3 no está o falla.

import threading
import subprocess
import sys


def _speak_windows_powershell(text):
    """Fallback en Windows: PowerShell + System.Speech.Synthesis (viene con Windows)."""
    clean = (text or "").strip().replace("'", "''").replace('"', '`"')
    if not clean:
        return
    # Escapar para PowerShell: comillas dobles y backticks
    escaped = clean.replace("\\", "\\\\").replace('"', '`"').replace("$", "`$")
    b64 = __import__("base64").b64encode(clean.encode("utf-8")).decode("ascii")
    cmd = [
        "powershell", "-NoProfile", "-NonInteractive", "-Command",
        "Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "try { $s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Neutral, [System.Speech.Synthesis.VoiceAge]::Adult, 0, [System.Globalization.CultureInfo]::GetCultureInfo('es')) } catch {}; "
        "$s.Rate = 0; $bytes = [System.Convert]::FromBase64String('%s'); $s.Speak([System.Text.Encoding]::UTF8.GetString($bytes))" % b64
    ]
    try:
        subprocess.run(cmd, timeout=120, capture_output=True, creationflags=0x08000000 if sys.platform == "win32" else 0)
    except Exception:
        # Sin Base64: texto corto directo (evitar caracteres raros)
        safe = "".join(c if ord(c) < 256 and c not in '"$\\`' else " " for c in clean)[:500]
        cmd2 = [
            "powershell", "-NoProfile", "-NonInteractive", "-Command",
            "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('%s')" % safe.replace("'", "''")
        ]
        try:
            subprocess.run(cmd2, timeout=120, capture_output=True, creationflags=0x08000000 if sys.platform == "win32" else 0)
        except Exception:
            pass


def _do_speak_pyttsx3(text):
    """Hablar con pyttsx3; guardamos motor global para poder hacer stop()."""
    global _engine_global
    try:
        import pyttsx3
        e = pyttsx3.init()
        _engine_global = e
        try:
            voices = e.getProperty("voices")
            for v in voices:
                name = (getattr(v, "name", None) or "").lower()
                vid = (getattr(v, "id", None) or "").lower()
                if "es" in name or "spanish" in name or "es_" in vid or "es-" in vid:
                    e.setProperty("voice", v.id)
                    break
        except Exception:
            pass
        e.setProperty("rate", 150)
        clean = (text or "").strip()
        if clean:
            e.say(clean)
            e.runAndWait()
    except Exception:
        pass
    finally:
        _engine_global = None


def _do_speak(text):
    clean = (text or "").strip()
    if not clean:
        return
    # Intentar pyttsx3 (en este hilo); si falla, en Windows usar PowerShell
    ok = False
    try:
        import pyttsx3
        _do_speak_pyttsx3(clean)
        ok = True
    except ImportError:
        pass
    except Exception:
        pass
    if not ok and sys.platform == "win32":
        _speak_windows_powershell(clean)


_engine_global = None  # Para poder llamar stop() desde el hilo principal (pyttsx3)


def speak(text):
    """Reproduce el texto en voz alta en segundo plano (no bloquea el juego)."""
    if not text or not str(text).strip():
        return
    t = threading.Thread(target=_do_speak, args=(str(text),), daemon=True)
    t.start()


def stop():
    """Detiene la reproducción de voz (solo con pyttsx3; PowerShell no se puede pausar)."""
    global _engine_global
    try:
        import pyttsx3
        if _engine_global is not None:
            _engine_global.stop()
    except Exception:
        pass


def is_available():
    """Indica si TTS está disponible."""
    if sys.platform == "win32":
        return True  # PowerShell SAPI disponible
    try:
        import pyttsx3
        pyttsx3.init()
        return True
    except Exception:
        return False
