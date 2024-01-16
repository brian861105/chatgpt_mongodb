import backend.src.openaiAPI as openaiAPI
from backend.src.Database import DatabaseManager

from flask import Flask, jsonify, request, Blueprint

GPT = openaiAPI.ChatGPT(MaxToken=500)
database = DatabaseManager()

linebot_receive_blueprint = Blueprint('linebot_receive', __name__)
@linebot_receive_blueprint.route("/linebot_receive_message", methods=["POST"])
def receive_message():
    data = request.json
    message_test = data["content"]
    OldMessage = []
    NewMessage = {"role": "user", "content": message_test}
    AImessage =GPT.Chat(OldMessage, NewMessage)[-1]["content"]
    ChatapiReply = {
        "role": "assistant",
        "content": AImessage,
    }

    return ChatapiReply, 200

database_blueprint = Blueprint('database', __name__)
@database_blueprint.route("/create_user", methods=["POST"])
def create_user(UserId="TestForFront"):
    return database.CreateUser(UserId=UserId)    

@database_blueprint.route("/read_user", methods=["GET"])
def read_user(UserId="TestForFront"):
    return database.ReadUser(UserId=UserId)  

@database_blueprint.route("/delete_user", methods=["DELETE"])
def delete_user(UserId="TestForFront"):    
    return database.DeleteUser(UserId=UserId)

@database_blueprint.route('/create_session', methods=["POST"])
def create_session():
    data = request.get_json()
    UserId = data.get("UserId")
    return database.CreateSession(UserId=UserId)

@database_blueprint.route('/read_session', methods=["POST"])
def read_session():
    data = request.get_json()
    UserId = data.get('UserId')
    SessionId = data.get('SessionId')
    
    return jsonify(database.ReadSession(UserId=UserId,SessionId=SessionId))


@database_blueprint.route('/rename_session', methods=["POST"])
def rename_session():
    data = request.get_json()
    
    UserId = data.get('UserId')
    SessionId = data.get('SessionId')
    NewTitle = data.get('NewTitle')
    result = database.RenameSessionTitle(UserId=UserId, SessionId=SessionId, NewTitle=NewTitle)
    return jsonify({'message': 'Session renamed successfully'})

@database_blueprint.route('/update_session', methods=["POST"])
def UpoloadMessage():
    data = request.get_json()
    
    UserId = data.get('UserId')
    SessionId = data.get('SessionId')
    message = data.get('message')
    OldMessage = database.ReadSession(UserId=UserId, SessionId=SessionId)["messages"]

    print(UserId, SessionId)
    InputOldMessage = []
    for i in range(len(OldMessage)):
        if i % 2:
            InputOldMessage.append({"role": "user", "content": OldMessage[i]})
        else:
            InputOldMessage.append({"role": "assistant", "content": OldMessage[i]})

    NewMessage = {"role": "user", "content": message}
    AImessage =GPT.Chat(InputOldMessage, NewMessage)[-1]["content"]
    ChatapiReply = {
        "role": "ChatGPT",
        "message": AImessage,
    }
    database.UpoloadMessage(UserId=UserId, SessionId=SessionId, NewMessage=message)
    database.UpoloadMessage(UserId=UserId, SessionId=SessionId, NewMessage=AImessage )
    return jsonify(ChatapiReply)

@database_blueprint.route('/delete_session', methods=["POST"])
def DeleteSession():
    data = request.get_json()
    
    UserId = data.get('UserId')
    SessionId = data.get('SessionId')
    
    database.DeleteSession(UserId=UserId, SessionId=SessionId)
    return jsonify({'message': 'Session removed successfully'})