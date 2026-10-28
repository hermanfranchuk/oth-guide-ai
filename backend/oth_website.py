import requests

# imports
from data import WEBSITE_PAGES, WEBSITE_PROMPT
from utils import download_html_page_text
from logger import logger, debug_print
from keyword_manager import keyword_match


# save extracted website texts
prepared_website_text = ""


# detect and load matching OTH website pages
def prepare_website_info(user_input):
    global prepared_website_text

    prepared_website_text = ""
    website_skill_needed = False

    for page in WEBSITE_PAGES:
        if keyword_match(user_input, page["tag"]):
            website_skill_needed = True

            try:
                debug_print("Loaded source: " + page["title"])
                prepared_website_text += download_html_page_text(page)
            except Exception as error:
                logger.warning("OTH website source could not be loaded: %s | %s", page["title"], error)

                prepared_website_text += (
                    f"Source title: {page['title']}\n"
                    f"Source URL: {page['url']}\n"
                    f"Error while loading this page: {error}\n\n"
                )

    return website_skill_needed


# return prepared text with special prompt
def website_info():
    global prepared_website_text

    result = WEBSITE_PROMPT + prepared_website_text
    prepared_website_text = ""

    return result