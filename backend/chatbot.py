import requests

# imports
from basic_info import read_basic_info
from mensa import mensa_info
from stundenplan import prepare_stundenplan_info, stundenplan_info
from oth_website import prepare_website_info, website_info
from stuv import prepare_stuv_info, stuv_info
from language import language_info
from logger import logger, debug_print
from keyword_manager import keyword_match
from chat_storage import get_next_chat_id, save_chat, load_chat_by_id, delete_chat
from datetime import date
from data import DATE_PROMPT
from config import BASE_URL, API_KEY, MODEL

# AI configuration is loaded from .env via config.py
# hide SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

start_messages = [
    {
        "role": "system",
        "content": "You are a helpful chatbot for OTH Regensburg website. Use the provided background information as internal context. Answer naturally, directly and friendly do not mention that you are using additional context or provided background information"
    },
    {
        "role": "user",
        "content": "Hello! You will answer my questions about OTH Regensburg website"
    }
]

data = {
    "model": MODEL,
    "messages": start_messages
}

# copy start messages to create first chat history
chat_history = start_messages.copy()


# chat history variables
current_chat_id = None
current_chat_title = None


# save current chat
def save_current_chat():
    if current_chat_id is not None and len(chat_history) > len(start_messages):
        save_chat(current_chat_id, current_chat_title, chat_history)


# start new chat
def start_new_chat():
    global chat_history
    global current_chat_id
    global current_chat_title

    save_current_chat()

    current_chat_id = get_next_chat_id()
    current_chat_title = f"Chat #{current_chat_id}"
    chat_history = start_messages.copy()

    logger.info("New chat started: %s", current_chat_id)

    return {
        "id": current_chat_id,
        "title": current_chat_title
    }


# open saved chat by id
def open_saved_chat(chat_id):
    global chat_history
    global current_chat_id
    global current_chat_title

    save_current_chat()

    chat = load_chat_by_id(chat_id)

    if chat is None:
        return None

    current_chat_id = chat["id"]
    current_chat_title = chat["title"]
    chat_history = chat["messages"]

    logger.info("Chat %s opened", chat_id)

    return chat


# delete saved chat by id
def delete_saved_chat(chat_id):
    global chat_history
    global current_chat_id
    global current_chat_title

    if current_chat_id == chat_id:
        current_chat_id = None
        current_chat_title = None
        chat_history = start_messages.copy()

        logger.debug("Active chat session %s was reset before deletion", chat_id)

    return delete_chat(chat_id)


# clear chat history to start a new conversation
def clear():
    global chat_history

    chat_history = start_messages.copy()


# use skills, send prompt to bot and give answer back
def ask_llm(use_date_skill, use_language_skill, use_basic_skill, use_mensa_skill, use_stundenplan_skill, use_website_skill, use_stuv_skill):
    global chat_history

    messages = chat_history.copy()

    current_date = date.today()
    current_weekday = current_date.strftime("%A")

    if use_date_skill:
        # add current date info
        debug_print("date will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": DATE_PROMPT.format(
                current_date=current_date.isoformat(),
                current_weekday=current_weekday
            )
        })

    if use_language_skill:
        # add language skill
        debug_print("language skill will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": language_info()
        })

    # add basic_info.txt as extra system context
    if use_basic_skill:
        debug_print("basic_info.txt will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": read_basic_info()
        })

    # add mensa menu as extra system context
    if use_mensa_skill:
        debug_print("mensa menu will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": mensa_info()
        })

    # add stundenplan as extra system context
    if use_stundenplan_skill:
        debug_print("stundenplan data will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": stundenplan_info()
        })

    # add oth_website as extra system context
    if use_website_skill:
        debug_print("website data will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": website_info()
        })

    # add stuv as extra system context
    if use_stuv_skill:
        debug_print("stuv data will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": stuv_info()
        })

    data["messages"] = messages

    logger.info("Sending LLM request for chat %s", current_chat_id)

    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/completions",
            headers=headers,
            json=data,
            verify=False
        )

        response.raise_for_status()

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        logger.info("LLM response received for chat %s", current_chat_id)
    except Exception:
        logger.exception("LLM request failed for chat %s", current_chat_id)
        raise

    # add bot answer to history
    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer


# get user input from frontend and return bot answer
def get_bot_answer(user_input):
    global chat_history

    # start new chat
    if current_chat_id is None:
        start_new_chat()

    # check if chat needs to be cleared
    if "/clear" in user_input:
        clear()
        debug_print("Chat cleared")
        return "Chat cleared"

    # add user request to history
    chat_history.append({
        "role": "user",
        "content": user_input
    })

    # no_skills mod
    if "/no_skills" in user_input:
        debug_print("No Skills")
        answer = ask_llm(False, False, False, False, False, False, False)
        save_current_chat()
        return answer

    # basic-skill check
    use_date_skill = True
    use_language_skill = True
    use_basic_skill = keyword_match(user_input, "BASIC")
    use_mensa_skill = keyword_match(user_input, "MENSA")
    use_stundenplan_skill = prepare_stundenplan_info(user_input)
    use_website_skill = prepare_website_info(user_input)
    use_stuv_skill = prepare_stuv_info(user_input)

    # return bot answer to frontend and save chat in history
    answer = ask_llm(use_date_skill, use_language_skill, use_basic_skill, use_mensa_skill, use_stundenplan_skill, use_website_skill, use_stuv_skill)
    save_current_chat()
    return answer