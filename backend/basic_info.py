# imports
from pathlib import Path
from utils import read_text_file
from logger import logger


# basic info file location
BASIC_INFO_FILE = Path(__file__).parent / "basic_info.txt"


# read text from basic_info.txt
def read_basic_info():
    return read_text_file(BASIC_INFO_FILE)