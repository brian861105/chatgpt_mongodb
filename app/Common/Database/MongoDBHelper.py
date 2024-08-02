# db/mongodb_helper.py
from pymongo import MongoClient
from Common.Database.iNoSqlDbHelper import iNoSqlDbHelper

class MongoDBHelper(iNoSqlDbHelper):
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"成功連接到 MongoDB 資料庫: {self.db_name}")
        except ConnectionError as e:
            print(f"無法連接到 MongoDB: {e}")
    
    def insert(self, collection: str, document: dict):
        try:
            self.db[collection].insert_one(document)
            print("插入文件成功")
        except Exception as e:
            print(f"插入文件失敗: {e}")
    
    def find(self, collection: str, query: dict):
        try:
            result = self.db[collection].find(query)
            return list(result)
        except Exception as e:
            print(f"查詢失敗: {e}")
            return None
    
    def update(self, collection: str, query: dict, update: dict):
        try:
            self.db[collection].update_many(query, {"$set": update})
            print("更新文件成功")
        except Exception as e:
            print(f"更新文件失敗: {e}")
    
    def delete(self, collection: str, query: dict):
        try:
            self.db[collection].delete_many(query)
            print("刪除文件成功")
        except Exception as e:
            print(f"刪除文件失敗: {e}")
    
    def closeConnection(self):
        if self.client:
            self.client.close()
            print("MongoDB 連接已關閉")
