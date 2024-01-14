import src.openaiAPI as openaiAPI
import src.Database as Database

from flask import Flask, jsonify, request, Blueprint

database = Database.mongo_client()
GPT = openaiAPI.ChatGPT()

backend_blueprint = Blueprint('linebot_receive_message', __name__)


@backend_blueprint.route("/", method=["POST"])
def receive_message():
    data = request.json
    user_id = data["user_id"]
    message_test = data["message_text"]
    OldMessage = []
    NewMessage = {"role": "user", "content": message_test}
    ChatapiReply = {
        "role": "assistant",
        "content": GPT.Chat(OldMessage, NewMessage)[-1]["content"],
    }

    return ChatapiReply, 200
