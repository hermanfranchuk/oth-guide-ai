import logging
from pathlib import Path

# imports
from data import LOG_LEVEL


# log file location
LOG_DIRECTORY = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIRECTORY / "app.log"
LOG_DIRECTORY.mkdir(exist_ok=True)


# convert text log level to logging constant
selected_log_level = getattr(
    logging,
    LOG_LEVEL.upper(),
    logging.INFO
)


# main project logger
logger = logging.getLogger("oth_guide_ai")
logger.setLevel(selected_log_level)
logger.propagate = False


# add handlers only once
if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # write all selected log levels to app.log
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setLevel(selected_log_level)
    file_handler.setFormatter(formatter)

    # show warnings and errors in console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# write debug messages
def debug_print(text):
    logger.debug(text)


# separate application launches in log file
def start_log_session(application_name):
    logger.info("=" * 60)
    logger.info("%s started", application_name)
    logger.info("=" * 60)