# from pymongo import MongoClient
from mongomock import MongoClient

class DatabaseManager:
    def __init__(self, mock_db=False, simulate_connection_failure = True):
        if mock_db:
            self.client = MongoClient()
            self.simulate_connection_failure = simulate_connection_failure
        else:
            self.client = MongoClient('mongodb://localhost:27017/')

        self.db_name = "test"
    def is_connect(self):
        try:
            if self.simulate_connection_failure:
                raise Exception("Simulated connection failure")
            self.client.server_info()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def create_collection(self, collection_name):
        try:
            
            self.client[self.db_name].insert_one(collection_name)
            return True
        except Exception as e:
            print(f"Collection creation error: {e}")
            return False
            