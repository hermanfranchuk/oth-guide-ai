import requests
import json

# imports
from pathlib import Path
from bs4 import BeautifulSoup
from logger import logger


# convert JSON data from a URL to readable text
def download_json_text(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    json_data = response.json()
    text = json.dumps(json_data, ensure_ascii=False, indent=2)

    logger.debug("JSON data loaded successfully from %s", url)

    return text


# extract readable text from an HTML page
def download_html_page_text(page):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(page["url"], headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    page_text = soup.get_text(separator=" ", strip=True)

    logger.debug("HTML page loaded successfully: %s", page["url"])

    return (
        f"Source title: {page['title']}\n"
        f"Source URL: {page['url']}\n"
        f"Page text:\n{page_text}\n\n"
    )


# read text from a local file
def read_text_file(file_path):
    try:
        file_path = Path(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        logger.debug("Text file loaded successfully: %s", file_path)
        return text

    except OSError:
        logger.exception("Text file could not be read: %s", file_path)
        raise

