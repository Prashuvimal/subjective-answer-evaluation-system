from spellchecker import SpellChecker
import re

spell = SpellChecker()

def correct_text(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    corrected = []

    for w in words:
        if len(w) <= 2:
            corrected.append(w)
        else:
            corrected.append(spell.correction(w) or w)

    return " ".join(corrected)
