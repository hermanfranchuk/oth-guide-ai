# imports
import json
import requests
from datetime import date, timedelta
from rapidfuzz import fuzz
from data import STUNDENPLAN_JSON_URL, STUNDENPLAN_PROMPT, STUNDENPLAN_SUBJECT_ALIASES, STUNDENPLAN_TEACHER_ALIASES, STUNDENPLAN_WEEKDAY_ALIASES, STUNDENPLAN_IGNORED_WORDS
from keyword_manager import keyword_match, normalize_text
from logger import logger


# prepared timetable text for the LLM prompt
prepared_stundenplan_text = ""


# collect useful search words from the user question
def get_search_words(user_input):
    text = normalize_text(user_input)
    words = text.split()
    search_words = []

    for word in words:
        if word in STUNDENPLAN_SUBJECT_ALIASES:
            search_words.extend(STUNDENPLAN_SUBJECT_ALIASES[word])

        if word in STUNDENPLAN_TEACHER_ALIASES:
            search_words.extend(STUNDENPLAN_TEACHER_ALIASES[word])

        if word in STUNDENPLAN_WEEKDAY_ALIASES:
            search_words.append(STUNDENPLAN_WEEKDAY_ALIASES[word])

        if len(word) >= 3 and word not in STUNDENPLAN_IGNORED_WORDS:
            search_words.append(word)

        if len(word) >= 3 and fuzz.partial_ratio(word, "room") >= 80 or fuzz.partial_ratio(word,"raum") >= 80:
            search_words.append("room")


    if "gestern" in text or "yesterday" in text:
        search_words.append((date.today() + timedelta(days=-1)).strftime("%A").lower())

    if "heute" in text or "today" in text:
        search_words.append(date.today().strftime("%A").lower())

    if "morgen" in text or "tomorrow" in text:
        search_words.append((date.today() + timedelta(days=1)).strftime("%A").lower())

    if "übermorgen" in text or "ubermorgen" in text:
        search_words.append((date.today() + timedelta(days=2)).strftime("%A").lower())

    cleaned_words = []

    for word in search_words:
        word = normalize_text(word).strip()

        if word and word not in cleaned_words:
            cleaned_words.append(word)

    return cleaned_words


# check if timetable block matches the user question
def block_matches_user_input(block, search_words):
    block_text = normalize_text(json.dumps(block, ensure_ascii=False))
    block_words = block_text.split()

    for word in search_words:
        if word in block_words or word in block_text:
            return True

        if len(word) > 4 and fuzz.partial_ratio(word, block_text) >= 90:
            return True

    return False


# prepare timetable data before LLM request
def prepare_stundenplan_info(user_input):
    global prepared_stundenplan_text

    prepared_stundenplan_text = ""

    if not keyword_match(user_input, "STUNDENPLAN"):
        return False

    try:
        response = requests.get(STUNDENPLAN_JSON_URL, timeout=20)
        response.raise_for_status()
        timetable_data = response.json()

        logger.debug("JSON data loaded successfully from %s", STUNDENPLAN_JSON_URL)

        search_words = get_search_words(user_input)
        matches = []

        if isinstance(timetable_data, dict):
            for key, value in timetable_data.items():
                block = {key: value}

                if block_matches_user_input(block, search_words):
                    matches.append(block)

        elif isinstance(timetable_data, list):
            for item in timetable_data:
                if block_matches_user_input(item, search_words):
                    matches.append(item)

        if matches:
            logger.debug("Stundenplan blocks: %s", str(len(matches)))
            prepared_stundenplan_text = json.dumps(
                matches[:25],
                ensure_ascii=False,
                indent=2
            )
        else:
            logger.warning("No filtered timetable match found, full JSON will be used")

            prepared_stundenplan_text = (
                "No exact pre-filter match was found. "
                "Use the following full timetable JSON carefully and try to answer from it.\n\n"
                + json.dumps(timetable_data, ensure_ascii=False, indent=2)
            )

        return True

    except Exception as error:
        logger.warning("Stundenplan data could not be loaded: %s", error)
        prepared_stundenplan_text = "Timetable data could not be loaded."
        return True


# return prepared timetable text with prompt
def stundenplan_info():
    global prepared_stundenplan_text

    result = STUNDENPLAN_PROMPT + prepared_stundenplan_text
    prepared_stundenplan_text = ""

    return result