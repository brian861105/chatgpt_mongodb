import backend.src.openaiAPI as openaiAPI
# import backend.src.Database as Database

from flask import Flask, jsonify, request, Blueprint

# database = Database.DatabaseManager()
GPT = openaiAPI.ChatGPT(MaxToken=500)

linebot_receive_blueprint = Blueprint('linebot_receive', __name__)
@linebot_receive_blueprint.route("/linebot_receive_message", methods=["POST"])
def receive_message():
    data = request.json
    # user_id = data["user_id"]
    message_test = data["content"]
    OldMessage = []
    NewMessage = {"role": "user", "content": message_test}
    ChatapiReply = {
        "role": "assistant",
        "content": GPT.Chat(OldMessage, NewMessage)[-1]["content"],
    }
    return ChatapiReply, 200
