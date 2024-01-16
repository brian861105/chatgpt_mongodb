# from mongomock import MongoClient
from pymongo import MongoClient
import json
import uuid
from datetime import datetime
import os

mongo_user = os.getenv("MongodbUser")
mongo_password = os.getenv("MongodbToken")
MongoURI = f"mongodb+srv://{mongo_user}:{mongo_password}@cluster0.7pgqvs4.mongodb.net/?retryWrites=true&w=majority"
class DatabaseManager:
    def __init__(self, SimulateConnectionFailure=True):
        self.client = MongoClient(MongoURI)
        self.database = self.client["my_database"]

    def IsConnect(self):
        try:
            if self.SimulateConnectionFailure:
                return False
            self.client.server_info()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def CreateUser(self, UserId):
        try:
            self.database[UserId].insert_one(
                {"UserId": UserId, "SessionId": "test session"}
            )
            return True
        except Exception as e:
            print(f"UserId creation error: {e}")
            return False

    def DeleteUser(self, UserId):
        try:
            collection = self.database[UserId]
            collection.drop()
            return True
        except Exception as e:
            print(f"UserId delete error: {e}")

    def ReadUser(self, UserId):
        try:
            collection = self.database[UserId]
            documents = collection.find()
            SessionList = [
                {"UserId": UserId, "SessionId": document.get("SessionId"), "Title": document.get("Title")}
                for document in documents
            ]
            SessionList = json.dumps(SessionList)
            return SessionList
        except Exception as e:
            print(f"UserId Read Error: {e}")

    def CreateSession(self, UserId):
        try:
            RandomSessionId = str(uuid.uuid4())
            collection = self.database[UserId]
            now = datetime.now()
            DateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
            ChatRoomDocument = {
                "UserId": UserId,
                "SessionId": RandomSessionId,
                "Title": "new title",
                "CreatedTime": DateTime,
                "messages": [],
            }
            collection.insert_one(ChatRoomDocument)
            del ChatRoomDocument["_id"]
            ReturnData = json.dumps(ChatRoomDocument)
            return ReturnData
        except Exception as e:
            print(f"Session Create Error: {e}")

    def DeleteSession(self, UserId, SessionId):
        try:
            collection = self.database[UserId]
            FilterCondition = {"SessionId": SessionId}
            result = collection.delete_one(FilterCondition)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Session Delete Error: {e}")
    def ReadSession(self, UserId, SessionId):
        try:
            Collection = self.database[UserId]
            FilterCondition = {"SessionId": SessionId}
            SessionContent = Collection.find_one(FilterCondition)
            del SessionContent["_id"]
            return SessionContent
        except Exception as e:
            print(f"Session Read Error: {e}")
        
    def RenameSessionTitle(self, UserId, SessionId, NewTitle):
        try:
            Collection = self.database[UserId]
            FilterCondition = {"SessionId": SessionId}
            UpdateOperation = {"$set": {"Title": NewTitle}}
            result = Collection.update_one(FilterCondition, UpdateOperation)
            return result.modified_count > 0
        except Exception as e:
            print(f"Session Rename Title Error: {e}")

    def UpoloadMessage(self, UserId, SessionId, NewMessage):
        try:
            Collection = self.database[UserId]
            FilterCondition = {"SessionId": SessionId}
            Messages = Collection.find_one({"SessionId": SessionId})["messages"]
            Messages.append(NewMessage)
            UpdateOperation = {"$set": {"messages": Messages}}
            result = Collection.update_one(FilterCondition, UpdateOperation)
            return result.modified_count > 0
        except Exception as e:
            print(f"Message Delivery Error: {e}")
