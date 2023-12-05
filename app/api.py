from flask import Flask, request, jsonify, make_response, abort
from flask_restful import Api, Resource
from datetime import datetime
import uuid

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import openai
from os.path import dirname, abspath
import sys

sys.path.append(dirname(dirname(abspath(__file__))))

from src.transfer_chatgpt import transfer_chat
import json
import os
# Open the JSON file and load its content
data_path = os.path.join(os.path.dirname(__file__), '..', 'tmp', 'key.json')
with open(data_path) as f:
    data = json.load(f)

mock_db = False
test_mode = True
chat_test = True

if(mock_db): 
    from mongomock import MongoClient as MockMongoClient
    client = MockMongoClient()
else:
    mg_password = data["mongodb"]
    uri = f"mongodb+srv://master:{mg_password}@cluster0.7pgqvs4.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client["mydatabase"]
user_collection = db["users"]

currentDateAndTime = datetime.now()
app = Flask(__name__)
api = Api(app)

if not chat_test:
    openai.api_key = data["openai"]

## 創建使用者/查詢使用者的所有session

class User(Resource):
    def post(self): ### create a session for user

        json_data = request.get_json()
        if not json_data:
            error_response = {"error": "JSON data is required"}
            return jsonify(error_response), 400
        error_response = {"error": "JSON data is required"}

        userId = json_data.get("user_name")
        if not userId:
            return {"error": "User ID is required"}, 400

        # # Your logic to create a new session
        # # Assuming request_data contains necessary fields
        try:
            currentDateAndTime = datetime.now().isoformat()
            new_session = {
                "user": userId,
                "messages": [],
                "title": "new_title",
                "sessionId": str(uuid.uuid4()),
                "createdAt": currentDateAndTime
            }
            user_collection.insert_one(new_session)
            del new_session["_id"]
            return make_response(jsonify(new_session), 201)

        except Exception as e:
            print(e)
            abort(500)
        

    def get(self, userId): ### get the data of user session 
        # Your logic to retrieve sessions for the given user ID
        # This is just a mock response for demonstration
        if not userId:
            return jsonify({"error": "User ID is required"}), 400
        try:    
            all_users = user_collection.find({"user" : userId})
            data_list = []
            for data in all_users:
                del data["_id"]
                data_list.append(data)
            json_response = jsonify(data_list)
            return make_response(json_response, 200)
        
        except Exception as e:
            print(e)
            abort(500)



class Session(Resource):
    def put(self, sessionId): ## update title
        new_title = request.args.get('title')
        request_data = request.get_json()

        if not sessionId or (not new_title and (not request_data or 'messages' not in request_data)):
            return {"error": "Either session ID is invalid or title does not exist"}, 400

        session = user_collection.find_one({"sessionId" : sessionId})
        filter_condition = {"sessionId" : sessionId}
        del session["_id"]
        if session:
            if new_title:
                session['title'] = new_title
                print(session['title'])
                return make_response(session, 200)
            new_message = request_data['messages']
            # Process message content (e.g., using OpenAI chat)
            # For demonstration purposes, adding a default response
            if chat_test:
                response_from_openAI = "Sorry, I don't understand."
                session['messages'].append(new_message)
                session['messages'].append(response_from_openAI)
            else:
                chat_history = session['messages']
                chat_history.append(new_message)
                chat_history = transfer_chat(chat_history)
                response_from_openAI = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_history
                )
                response_from_openAI = response_from_openAI.choices[0].message.content
                session['messages'].append(new_message)
                session['messages'].append(response_from_openAI)
            new_session = dict()
            new_session["$set"] = session
            result = user_collection.update_one(filter_condition, new_session)

            if result.modified_count == 0:
                return {"error": "Either session ID is invalid or title does not exist"}, 400

            return make_response(session, 200)
        else:
            return {"error": "Session not found"}, 404

    def delete(self, sessionId):
        if not sessionId:
            return {"error": "Session ID is required"}, 400
        session = user_collection.find_one({"sessionId" : sessionId})

        if len(session):
            user_collection.delete_one({ "sessionId" :sessionId})
            return {"message": "Session deleted"}, 200
        else:
            return {"error": "Session not found"}, 404

    def get(self, sessionId): ### get the data of user session 
        # Your logic to retrieve sessions for the given user ID
        # This is just a mock response for demonstration
        if not sessionId:
            return {"error": "Session ID is required"}, 400
        
        try:
            session = user_collection.find_one({"sessionId" : sessionId})

            del session["_id"]


            return make_response(jsonify(session), 200)
        
        except Exception as e:
            print(e)
            abort(500)



api.add_resource(Session, '/session/<string:sessionId>')
api.add_resource(User, '/user', '/user/<string:userId>/sessions')

if __name__ == '__main__':

    app.run(debug=test_mode)