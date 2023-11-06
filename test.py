from flask import Flask, request
from flasgger import Swagger
from flask_restful import Api, Resource
from datetime import datetime

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

sessions_data = [
     {
        "session_id": "session_id_1",
        "user": "user_1",
        "title": "Session 1",
        "messages": ["Message 1", "Message 2"],
        "createdAt": currentDateAndTime
    },
     {
        "session_id": "session_id_1",
        "user": "user_1",
        "title": "Session 1",
        "messages": ["Message 3", "Message 4"],
        "createdAt": currentDateAndTime + 10
    },
    {
        "session_id": "session_id_2",
        "user": "user_2",
        "title": "Session 2",
        "messages": ["Hello", "Hi"],
        "createdAt": datetime.now() - 10
    }
]

class UserSession(Resource):
    def post(self, userId): ### create a session for user
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
        user_id = userId
        request_data = request.get_json()

        if not user_id:
            return {"error": "User ID is required"}, 400

        # Your logic to create a new session
        # Assuming request_data contains necessary fields
        new_session = {
            "user": request_data.get("user"),
            "title": request_data.get("title"),
            "createdAt": request_data.get("createdAt"),
            "messages": request_data.get("messages", [])
        }
        if new_session:
            inserted_data = user_collection.insert_one(sessions_data)
            if inserted_data:
                print("Successful insert")
                new_session_id = inserted_data.inserted_id
                new_session["_id"] = new_session_id
            else:
                print("insert data error")

        return new_session, 201

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

        return userId, 200



class Session(Resource):
    def put(self, sessionId):
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

        if not sessionId or (not new_title and (not request_data or 'content' not in request_data)):
            return {"error": "Content and sessionId are required"}, 400

        session = sessions_data.get(sessionId)

        if session:
            if new_title:
                session['title'] = new_title
                return session, 200

            new_message = request_data['content']
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

        if sessionId in sessions_data:
            del sessions_data[sessionId]
            return {"message": "Session deleted"}, 200
        else:
            return {"error": "Session not found"}, 404

api.add_resource(Session, '/session/<string:sessionId>')
api.add_resource(UserSession, '/users/<string:userId>/sessions')

if __name__ == '__main__':
    app.run(debug=True)
