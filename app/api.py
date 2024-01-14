from flask import Flask, request, jsonify, make_response, abort
from flask_restful import Api, Resource
from datetime import datetime
import uuid
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import openai
import json
import os
from flasgger import Swagger, swag_from

mg_password = os.getenv('MongoDBToken')


## test
class DatabaseManager:

    def __init__(self, mock_db=False):
        if mock_db:
            from mongomock import MongoClient as MockMongoClient
            self.client = MockMongoClient()
        else:
            uri = f"mongodb+srv://master:{mg_password}@cluster0.7pgqvs4.mongodb.net/?retryWrites=true&w=majority"
            self.client = MongoClient(uri, server_api=ServerApi('1'))

        try:
            self.client.admin.command('ping')
            print(
                "Pinged your deployment. You successfully connected to MongoDB!"
            )
        except Exception as e:
            print(e)

        self.db = self.client["mydatabase"]
        self.user_collection = self.db["users"]


class UserResource(Resource):

    def __init__(self, database_manager):
        self.db = database_manager
        self.current_date_and_time = datetime.now().isoformat()

    @swag_from({
        'tags': ['users'],
        'parameters': [{
            'in': 'body',
            'name': 'User_name',
            'schema': {
                'id': 'User',
                'required': ['user_name'],
                'example': {
                    'user_name': 'SINOPAC'
                }
            }
        }],
        'responses': {
            201: {
                'description': 'User created successfully',
                'examples': {
                    'User_id': 'User created successfully'
                }
            },
            400: {
                'description': 'Bad request'
            }
        }
    })
    def post(self):
        """
        Create a new user session.
        """
        json_data = request.get_json()
        if not json_data:
            error_response = {"error": "JSON data is required"}
            return jsonify(error_response), 400

        user_id = json_data.get("user_name")
        if not user_id:
            return {"error": "User ID is required"}, 400
        try:
            new_session = {
                "user": user_id,
                "messages": [],
                "title": "new_title",
                "sessionId": str(uuid.uuid4()),
                "createdAt": self.current_date_and_time
            }
            self.db.user_collection.insert_one(new_session)
            del new_session["_id"]
            return make_response(jsonify(new_session), 201)
        except Exception as e:
            print(e)
            abort(500)

    @swag_from({
        'tags': ['users'],
        'parameters': [{
            'in': 'query',
            'name': 'user_id',
            'type': 'string',
            'example': 'SINOPAC',
            'required': True
        }],
        'responses': {
            200: {
                'description':
                'User sessions retrieved successfully',
                'examples': [{
                    'user': 'john',
                    'sessionId': '1234'
                }, {
                    'user': 'jane',
                    'sessionId': '5678'
                }]
            },
            400: {
                'description': 'Bad request'
            }
        }
    })
    def get(self):
        """
        Get user sessions by user ID.
        """
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        try:
            all_users = self.db.user_collection.find({"user": user_id})
            data_list = [{
                "user": data["user"],
                "sessionId": data["sessionId"]
            } for data in all_users]
            print(data_list)
            return make_response(data_list, 200)
        except Exception as e:
            print(e)
            abort(500)


class SessionResource(Resource):

    def __init__(self, database_manager, mockChatgpt):
        self.db = database_manager
        self.mockChatgpt = mockChatgpt

    @swag_from({
        'tags': ['sessions'],
        'parameters': [{
            'in': 'path',
            'name': 'session_id',
            'type': 'string',
            'required': True
        }, {
            'in': 'query',
            'name': 'title',
            'type': 'string'
        }, {
            'in': 'body',
            'name': 'user_messages',
            'schema': {
                'id': 'Session',
                'example': {
                    'messages': 'hello world'
                }
            }
        }],
        'responses': {
            200: {
                'description': 'Session details retrieved successfully',
            },
            400: {
                'description': 'Bad request'
            },
            404: {
                'description': 'Session not found'
            }
        }
    })
    def put(self, session_id):
        """
        Update session details.
        """
        new_title = request.args.get('title')
        request_data = request.get_json()

        if not session_id or (not new_title and
                              (not request_data
                               or 'messages' not in request_data)):
            return {
                "error": "Either session ID is invalid or title does not exist"
            }, 400

        session = self.db.user_collection.find_one({"sessionId": session_id})
        if not session:
            return {"error": "Session not found"}, 404

        del session["_id"]

        if new_title:
            session['title'] = new_title
        new_message = request_data['messages']
        # Process message content (e.g., using OpenAI chat)
        # For demonstration purposes, adding a default response
        session['messages'].append(new_message)

        if (self.mockChatgpt):
            response_from_openai = "Sorry, I don't understand."
        else:
            with open(
                    os.path.join(os.path.dirname(__file__), '..', 'tmp',
                                 'key.json')) as f:
                key_json = json.load(f)
            openai_password = key_json["openai"]
            openai.api_key = openai_password
            chat_history = []
            for i in range(len(session['messages'])):
                if (i % 2):
                    role = "assistant"
                else:
                    role = "user"
                chat_history.append({
                    "role": role,
                    "content": session['messages'][i]
                })
            response_from_openai = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_history).choices[0].message.content
        session['messages'].append(response_from_openai)

        new_session = {"$set": session}
        result = self.db.user_collection.update_one({"sessionId": session_id},
                                                    new_session)

        if result.modified_count == 0:
            return {
                "error": "Either session ID is invalid or title does not exist"
            }, 400

        return make_response(session, 200)

    @swag_from({
        'tags': ['sessions'],
        'parameters': [{
            'in': 'path',
            'name': 'session_id',
            'type': 'string',
            'required': True
        }],
        'responses': {
            200: {
                'description': 'Session deleted successfully.',
                'examples': {
                    'sessionId': '1234'
                }
            },
            400: {
                'description': 'Bad request'
            },
            404: {
                'description': 'Session not found'
            }
        }
    })
    def delete(self, session_id):
        """
        Delete a session.
        """
        if not session_id:
            return {"error": "Session ID is required."}, 400

        session = self.db.user_collection.find_one({"sessionId": session_id})
        if session:
            self.db.user_collection.delete_one({"sessionId": session_id})
            return {"message": "Session deleted"}, 200
        else:
            return {"error": "Session not found"}, 404

    @swag_from({
        'tags': ['sessions'],
        'parameters': [{
            'in': 'path',
            'name': 'session_id',
            'type': 'string',
            'required': True
        }],
        'responses': {
            200: {
                'description': 'Get session details by session ID.',
                'examples': {
                    'sessionId': '1234'
                }
            },
            400: {
                'description': 'Bad request'
            },
            404: {
                'description': 'Session not found'
            }
        }
    })
    def get(self, session_id):
        """
        Get session details by session ID.
        """
        if not session_id:
            return {"error": "Session ID is required"}, 400

        try:
            session = self.db.user_collection.find_one(
                {"sessionId": session_id})
            del session["_id"]
            return make_response(jsonify(session), 200)
        except Exception as e:
            print(e)
            abort(500)


app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
database_manager = DatabaseManager(mock_db=False)
api.add_resource(UserResource,
                 '/user',
                 resource_class_kwargs={'database_manager': database_manager})
api.add_resource(SessionResource,
                 '/session/<string:session_id>',
                 resource_class_kwargs={
                     'database_manager': database_manager,
                     'mockChatgpt': False
                 })

if __name__ == '__main__':
    docker = True
    if docker:
        app.run(debug=True, host="0.0.0.0")
    else:
        app.run(debug=True)
