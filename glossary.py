# Glosario Nasa Yuwe: palabras que el jugador va desbloqueando (por zona, máscara o recogiendo)

# Cada palabra: id, español, nasa yuwe, categoría, desbloqueo (zona o máscara o "pickup")
# Categorías por nivel: 1=animales, 2=familia, 3=saludos, 4=naturaleza, 5=lugares, 6=máscaras
GLOSSARY_WORDS = [
    {"id": "nasa", "es": "pueblo / gente", "nasa": "Nasa", "category": "lugares", "unlock": "zone", "unlock_id": "pueblo_1"},
    {"id": "yat", "es": "casa", "nasa": "yat", "category": "lugares", "unlock": "zone", "unlock_id": "pueblo_1"},
    {"id": "yu", "es": "agua", "nasa": "Yu'", "category": "naturaleza", "unlock": "zone", "unlock_id": "pueblo_2"},
    {"id": "cxwa", "es": "máscara", "nasa": "Cxwa'", "category": "máscaras", "unlock": "zone", "unlock_id": "pueblo_1"},
    {"id": "magapete", "es": "hola (buenos días)", "nasa": "Ma'ga pe'te", "category": "saludos", "unlock": "zone", "unlock_id": "pueblo_2"},
    {"id": "kiputxuynhaw", "es": "adiós", "nasa": "Ki putxuynha'w", "category": "saludos", "unlock": "zone", "unlock_id": "cumbre_1"},
    {"id": "kiwe", "es": "tierra / bosque", "nasa": "Kiwe", "category": "naturaleza", "unlock": "zone", "unlock_id": "bosque_1"},
    {"id": "thej", "es": "cueva", "nasa": "The'j", "category": "lugares", "unlock": "zone", "unlock_id": "cueva_1"},
    {"id": "piyayu", "es": "santuario final", "nasa": "Piyayu'", "category": "lugares", "unlock": "zone", "unlock_id": "santuario_final"},
    # Palabras que se recogen (pickup) — animales, familia, etc.
    {"id": "mishi", "es": "gato", "nasa": "Mishi", "category": "animales", "unlock": "pickup"},
    {"id": "alcu", "es": "perro", "nasa": "alcu", "category": "animales", "unlock": "pickup"},
    {"id": "cuchi", "es": "cerdo", "nasa": "cuchi", "category": "animales", "unlock": "pickup"},
    {"id": "tul", "es": "huerta / cultivo", "nasa": "Tul", "category": "naturaleza", "unlock": "pickup"},
    {"id": "piyayat", "es": "escuela", "nasa": "Piya yat", "category": "lugares", "unlock": "pickup"},
]

# Máscaras: nombre en Nasa Yuwe y animal que la representa (presentación "Ma'ga pe'te, yo soy X")
MASK_NASA_NAMES = {
    "fly": {"nasa": "Cxwa' wala", "animal": "Mishi", "animal_es": "gato"},
    "swim": {"nasa": "Yu'", "animal": "Wayra", "animal_es": "pez"},
    "secrets": {"nasa": "Ver lo escondido", "animal": "Kwe'sx", "animal_es": "ave"},
    "doors": {"nasa": "Abrir Yat", "animal": "Tëj", "animal_es": "guardían"},
    "double": {"nasa": "The'j salto", "animal": "Sëkx", "animal_es": "sapo"},
    "dash": {"nasa": "Rayo", "animal": "Kwsx", "animal_es": "rayo"},
    "speed": {"nasa": "Nasa Kiwe", "animal": "We'sx", "animal_es": "venado"},
    "strong": {"nasa": "Kiwe u'", "animal": "Yu'j", "animal_es": "oso"},
    "shield": {"nasa": "Escudo", "animal": "Tëj", "animal_es": "guardían"},
    "final": {"nasa": "Piyayu'", "animal": "Mayor", "animal_es": "sabio"},
}


def get_word_by_id(word_id):
    for w in GLOSSARY_WORDS:
        if w["id"] == word_id:
            return w
    return None


def get_words_for_zone(zone_or_room_id):
    return [w for w in GLOSSARY_WORDS if w.get("unlock") == "zone" and w.get("unlock_id") == zone_or_room_id]


def get_words_for_mask(mask_id):
    # Palabras que se desbloquean al conseguir una máscara (opcional)
    return []


def get_categories():
    cats = set(w["category"] for w in GLOSSARY_WORDS)
    return sorted(cats)


def get_words_by_category(category):
    return [w for w in GLOSSARY_WORDS if w["category"] == category]
