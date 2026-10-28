from flask import Flask, request, jsonify
from flask_cors import CORS


# imports
from chatbot import get_bot_answer, start_new_chat, open_saved_chat, delete_saved_chat
from chat_storage import load_chat_titles
from logger import start_log_session


# flask
app = Flask(__name__)
CORS(app)


# frontend <--> backend connection
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    user_message = data.get("message")

    bot_answer = get_bot_answer(user_message)

    return jsonify({
        "answer": bot_answer
    })

@app.route("/new_chat", methods=["POST"])
def new_chat():
    chat_info = start_new_chat()

    return jsonify(chat_info)

@app.route("/chats_titles", methods=["GET"])
def chats_titles():
    chat_titles = load_chat_titles()

    return jsonify({
        "chats": chat_titles
    })

@app.route("/chat/<int:chat_id>", methods=["GET"])
def chat(chat_id):
    chat_info = open_saved_chat(chat_id)

    return jsonify(chat_info)

@app.route("/chat/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    chat_deleted = delete_saved_chat(chat_id)

    if not chat_deleted:
        return jsonify({
            "deleted": False,
            "message": "Chat not found"
        }), 404

    return jsonify({
        "deleted": True,
        "id": chat_id
    })



# application
if __name__ == "__main__":
    start_log_session("Web application")
    app.run(debug=True, port=5000)