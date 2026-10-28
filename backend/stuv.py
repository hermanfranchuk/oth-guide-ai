# imports
from data import STUV_PAGES, STUV_PROMPT
from utils import download_html_page_text
from logger import logger, debug_print
from keyword_manager import keyword_match


# save extracted website texts
prepared_stuv_text = ""


# load matching STUV website pages
def add_stuv_page_text(page):
    if page is None:
        return ""

    result = ""
    for source in page["sources"]:
        try:
            debug_print("Loaded source: " + source["title"])
            result += download_html_page_text(source)
        except Exception as error:
            logger.warning("StuV source could not be loaded: %s | %s", source["title"], error)

            result += (
                f"Source title: {source['title']}\n"
                f"Source URL: {source['url']}\n"
                f"Error while loading this page: {error}\n\n"
            )

    return result


# detect matching STUV website pages
def prepare_stuv_info(user_input):
    global prepared_stuv_text

    prepared_stuv_text = ""
    stuv_skill_needed = False
    base_page = None

    for page in STUV_PAGES:
        if page.get("base"):
            base_page = page

        if keyword_match(user_input, page["tag"]):
            stuv_skill_needed = True

            if not page.get("base"):
                prepared_stuv_text += add_stuv_page_text(page)

    if not stuv_skill_needed:
        prepared_stuv_text = ""
        return False

    if base_page is not None:
        prepared_stuv_text = add_stuv_page_text(base_page) + prepared_stuv_text

    return True


# return prepared text with special prompt
def stuv_info():
    global prepared_stuv_text

    result = STUV_PROMPT + prepared_stuv_text
    prepared_stuv_text = ""

    return result