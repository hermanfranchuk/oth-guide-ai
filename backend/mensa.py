# imports
from data import MENSA_JSON_URL, MENSA_PROMPT
from utils import download_json_text
from logger import logger


# parse menu info from URL to return with special prompt
def mensa_info():
    try:
        text = download_json_text(MENSA_JSON_URL)
        return MENSA_PROMPT + text
    except Exception as error:
        logger.warning("Mensa data could not be loaded: %s", error)