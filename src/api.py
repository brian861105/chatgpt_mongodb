from flask import Flask, request, jsonify, make_response, abort
from flasgger import Swagger
from flask_restful import Api, Resource
from datetime import datetime
import uuid


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

password = "WyJRepqRLIZ7K5CJ"
uri = f"mongodb+srv://master:{password}@cluster0.7pgqvs4.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

# test
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

swagger = Swagger(app)

## 創建使用者/查詢使用者的所有session

class User(Resource):
    def post(self): ### create a session for user
        """
        Create a new session for a user by ID
        ---
        tags:
          - users
        parameters:
          - name: userId
            in: path
            type: string
            required: true
            description: ID of the user
          - name: body
            in: body
            required: true
            schema:
              properties:
                user:
                  type: string
                  description: Name of the user
                title:
                  type: string
                  description: Title of the session
                createdAt:
                  type: string
                  format: date-time
                  description: Date and time of session creation
                messages:
                  type: array
                  items:
                    type: string
                  description: Array of messages
        responses:
          201:
            description: Successful creation
            schema:
              properties:
                _id:
                  type: string
                user:
                  type: string
                title:
                  type: string
                createdAt:
                  type: string
                  format: date-time
                messages:
                  type: array
                  items:
                    type: string
          400:
            description: User ID not provided
            schema:
              properties:
                error:
                  type: string
                  description: User ID is required
          500:
            description: Internal server error
            schema:
              properties:
                error:
                  type: string
                  description: Internal Server Error
        """
        userId = request.get_json().get("user_name")

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
            inserted_data = user_collection.insert_one(new_session)
            del new_session["_id"]
            return make_response(jsonify(new_session), 201)

        except Exception as e:
            print(e)
            abort(500)
        

    def get(self, userId): ### get the data of user session 
        """
        Retrieve sessions for a user by ID
        ---
        tags:
          - users
        parameters:
          - name: userId
            in: path
            type: string
            required: true
            description: ID of the user
        responses:
          200:
            description: Successful retrieval
            schema:
              type: array
              items:
                properties:
                  _id:
                    type: string
                  user:
                    type: string
                  title:
                    type: string
                  createdAt:
                    type: string
                    format: date-time
          400:
            description: User ID not provided
            schema:
              properties:
                error:
                  type: string
                  description: User ID is required
          500:
            description: Internal server error
            schema:
              properties:
                error:
                  type: string
                  description: Internal Server Error
        """
        # Your logic to retrieve sessions for the given user ID
        # This is just a mock response for demonstration
        if not userId:
            return {"error": "User ID is required"}, 400

        try:    
            all_users = user_collection.find({"user" : userId})
            data_list = []
            for data in all_users:
                del data["_id"]
                data_list.append(data)

            return make_response(jsonify(data_list), 200)
        
        except Exception as e:
            print(e)
            abort(500)

api.add_resource(User, '/user', '/user/<string:user_name>/sessions')

class Session(Resource):
    def put(self, sessionId): ## update title
        """
        Update session title or add a message by session ID
        ---
        tags:
          - sessions
        parameters:
          - name: sessionId
            in: path
            type: string
            required: true
            description: ID of the session
          - name: title
            in: query
            type: string
            description: New title for the session (optional)
          - name: body
            in: body
            required: true
            schema:
              properties:
                content:
                  type: string
                  description: Content of the message to add (optional)
        responses:
          200:
            description: Successful title update or message addition with OpenAI chat result or default response
            schema:
              properties:
                _id:
                  type: string
                user:
                  type: string
                title:
                  type: string
                messages:
                  type: array
                  items:
                    type: string
                createdAt:
                  type: string
                  format: date-time
          400:
            description: Content or sessionId not provided
            schema:
              properties:
                error:
                  type: string
                  description: Content and sessionId are required
          404:
            description: Session not found
            schema:
              properties:
                error:
                  type: string
                  description: Session not found
          500:
            description: Internal server error
            schema:
              properties:
                error:
                  type: string
                  description: Internal Server Error
        """
        new_title = request.args.get('title')
        request_data = request.get_json()
        print(not new_title or (not request_data or 'messages' not in request_data))
        if not sessionId or (not new_title and (not request_data or 'messages' not in request_data)):
            return {"error": "Either session ID is invalid or title does not exist"}, 400

        session = user_collection.find_one({"session_id" : sessionId})
        del session["_id"]
        if session:
            if new_title:
                session['title'] = new_title
                print(session['title'])
                return session, 200
            new_message = request_data['messages']
            # Process message content (e.g., using OpenAI chat)
            # For demonstration purposes, adding a default response
            response_from_openAI = "Sorry, I don't understand."
            session['messages'].append(new_message)
            session['messages'].append(response_from_openAI)
            return session, 200
        else:
            return {"error": "Session not found"}, 404

    def delete(self, sessionId):
        """
        Delete session by session ID
        ---
        tags:
          - sessions
        parameters:
          - name: sessionId
            in: path
            type: string
            required: true
            description: ID of the session
        responses:
          200:
            description: Successful deletion
            schema:
              properties:
                message:
                  type: string
                  description: Session deleted
          400:
            description: Session ID not provided
            schema:
              properties:
                error:
                  type: string
                  description: Session ID is required
          404:
            description: Session not found
            schema:
              properties:
                error:
                  type: string
                  description: Session not found
          500:
            description: Internal server error
            schema:
              properties:
                error:
                  type: string
                  description: Internal Server Error
        """
        if not sessionId:
            return {"error": "Session ID is required"}, 400
        session = user_collection.find_one({"session_id" : sessionId})

        if len(session):
            user_collection.delete_one({ "session_id" :sessionId})
            return {"message": "Session deleted"}, 200
        else:
            return {"error": "Session not found"}, 404

    def get(self, sessionId): ### get the data of user session 
        """
        Retrieve sessions for a user by ID
        ---
        tags:
          - users
        parameters:
          - name: userId
            in: path
            type: string
            required: true
            description: ID of the user
        responses:
          200:
            description: Successful retrieval
            schema:
              type: array
              items:
                properties:
                  _id:
                    type: string
                  user:
                    type: string
                  title:
                    type: string
                  createdAt:
                    type: string
                    format: date-time
          400:
            description: User ID not provided
            schema:
              properties:
                error:
                  type: string
                  description: User ID is required
          500:
            description: Internal server error
            schema:
              properties:
                error:
                  type: string
                  description: Internal Server Error
        """
        # Your logic to retrieve sessions for the given user ID
        # This is just a mock response for demonstration
        if not sessionId:
            return {"error": "Session ID is required"}, 400
        
        try:
            session = user_collection.find_one({"session_id" : sessionId})

            del session["_id"]


            return make_response(jsonify(session), 200)
        
        except Exception as e:
            print(e)
            abort(500)



api.add_resource(Session, '/session/<string:sessionId>')


if __name__ == '__main__':
    app.run(debug=True)
