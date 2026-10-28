import requests

# imports
from basic_info import read_basic_info
from mensa import mensa_info
from stundenplan import prepare_stundenplan_info, stundenplan_info
from oth_website import prepare_website_info, website_info
from stuv import prepare_stuv_info, stuv_info
from language import language_info
from logger import logger, debug_print, start_log_session
from keyword_manager import keyword_match
from datetime import date
from data import DATE_PROMPT
from config import BASE_URL, API_KEY, MODEL

# AI configuration is loaded from .env via config.py
# hide SSL warnings because verify=False is used
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful chatbot for OTH Regensburg website. Use the provided background information as internal context. Answer naturally, directly and friendly do not mention that you are using additional context or provided background information"
        },
        {
            "role": "user",
            "content": "Hello! You will answer my questions about OTH Regensburg website"
        }
    ]
}

response = requests.post(
    f"{BASE_URL}/api/chat/completions",
    headers=headers,
    json=data,
    verify=False
)

# copy start messages to create first chat history
chat_history = data["messages"].copy()


# clear chat history to start a new conversation
def clear():
    global chat_history
    chat_history = [
        {
            "role": "system",
            "content": "You are a helpful chatbot for OTH Regensburg website. Use the provided background information as internal context. Answer naturally, directly and friendly do not mention that you are using additional context or provided background information"
        },
        {
            "role": "user",
            "content": "Hello! You will answer my questions about OTH Regensburg website"
        }
    ]


# use skills, send prompt to bot and give answer back
def ask_llm(use_date_skill, use_language_skill, use_basic_skill, use_mensa_skill, use_stundenplan_skill, use_website_skill, use_stuv_skill):
    global chat_history

    messages = chat_history.copy()

    current_date = date.today()
    current_weekday = current_date.strftime("%A")

    # add current date info
    if use_date_skill:
        debug_print("date will be added to prompt")
        messages.insert(1, {
            "role": "system",
            "content": DATE_PROMPT.format(
                current_date=current_date.isoformat(),
                current_weekday=current_weekday
            )
        })

    # add language skill
    if use_language_skill:
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

    logger.info("Sending LLM request from console application")

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

        logger.info("LLM response received in console application")
    except Exception:
        logger.exception("LLM request failed in console application")
        raise

    # add bot answer to history
    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer


# start bot message
start_log_session("Console application")
answer = ask_llm(False, False,False, False, False, False, False)
print("Bot:", answer)

# conversation
while True:
    # reading user input
    user_input = input("Your request: ")

    # check if chat needs to be cleared
    if "/clear" in user_input:
        clear()
        debug_print("Chat cleared")
    else:
        # no_skills mod
        if "/no_skills" in user_input:
            debug_print("No Skills")

            chat_history.append({
                "role": "user",
                "content": user_input
            })

            answer = ask_llm(False, False, False, False, False, False, False)
            print("Bot:", answer)
        else:
            # add user request to history
            chat_history.append({
                "role": "user",
                "content": user_input
            })

            # basic-skill check
            use_date_skill = True
            use_language_skill = True
            use_basic_skill = keyword_match(user_input, "BASIC")
            use_mensa_skill = keyword_match(user_input, "MENSA")
            use_stundenplan_skill = prepare_stundenplan_info(user_input)
            use_website_skill = prepare_website_info(user_input)
            use_stuv_skill = prepare_stuv_info(user_input)

            # write answer in console
            answer = ask_llm(use_date_skill, use_language_skill, use_basic_skill, use_mensa_skill, use_stundenplan_skill, use_website_skill, use_stuv_skill)
            print("Bot:", answer)


