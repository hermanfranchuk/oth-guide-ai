# imports
from data import LANGUAGE_PROMPT, LANGUAGE_TERMS


# prepare and add glossary information to return with special prompt
def language_info():
    text = LANGUAGE_PROMPT

    for term in LANGUAGE_TERMS:
        parts = []

        if "german" in term:
            parts.append(f"German term: {term['german']}")

        if "english" in term:
            parts.append(f"English translation: {term['english']}")

        if "abbreviation" in term:
            parts.append(f"Abbreviation: {term['abbreviation']}")

        if "explanation" in term:
            parts.append(f"Simple explanation: {term['explanation']}")

        text += " | ".join(parts) + "\n"

    return text