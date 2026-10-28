import json
from pathlib import Path


#imports
from logger import logger


# save information in chat_history.json
CHAT_HISTORY_FILE = Path(__file__).parent / "chat_history.json"



# load chats
def load_chats():
    if not CHAT_HISTORY_FILE.exists():
        logger.warning("Chat history file does not exist; empty history will be used")
        return []

    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if content == "":
            logger.debug("Chat history file is empty")
            return []

        chats = json.loads(content)
        return chats

    except (OSError, json.JSONDecodeError):
        logger.exception("Chat history file could not be loaded")
        raise


# get next chat id
def get_next_chat_id():
    chats = load_chats()

    if not chats:
        return 1

    return chats[-1]["id"] + 1


# save chat
def save_chat(chat_id, title, messages):
    chats = load_chats()

    new_chat = {
        "id": chat_id,
        "title": title,
        "messages": messages
    }

    for index in range(len(chats)):
        if chats[index]["id"] == chat_id:
            chats[index] = new_chat
            break
    else:
        chats.append(new_chat)

    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chats, file, ensure_ascii=False, indent=4)

    logger.info("Chat %s saved", chat_id)


# load chat titles
def load_chat_titles():
    chats = load_chats()

    chat_titles = []

    for chat in chats:
        chat_titles.append({
            "id": chat["id"],
            "title": chat["title"]
        })

    return chat_titles


# load chat by id
def load_chat_by_id(chat_id):
    chats = load_chats()

    for chat in chats:
        if chat["id"] == chat_id:
            return chat

    logger.warning("Chat %s was not found", chat_id)
    return None


# delete chat by id
def delete_chat(chat_id):
    chats = load_chats()

    updated_chats = []

    for chat in chats:
        if chat["id"] != chat_id:
            updated_chats.append(chat)

    if len(updated_chats) == len(chats):
        logger.warning("Chat %s could not be deleted because it was not found", chat_id)
        return False

    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_chats, file, ensure_ascii=False, indent=4)

    logger.info("Chat %s deleted", chat_id)
    return True