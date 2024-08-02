import unittest
from unittest.mock import patch
from mongomock import MongoClient as MockMongoClient
from Common.Database.MongoDBHelper import MongoDBHelper

class TestMongoDBHelper(unittest.TestCase):
    def setUp(self):
        # 使用 MongoDB mock
        self.mock_client = MockMongoClient()
        self.db_name = 'test_db'
        self.collection_name = 'test_collection'
        self.helper = MongoDBHelper(uri='mongodb://localhost:27017', db_name=self.db_name)
        self.helper.client = self.mock_client
        self.helper.db = self.mock_client[self.db_name]

    def tearDown(self):
        self.helper.closeConnection()

    def test_connect(self):
        # 使用 mock 的 MongoClient，因此无需实际连接
        self.helper.connect()
        self.assertEqual(self.helper.db.name, self.db_name)

    def test_insert(self):
        document = {"name": "Alice", "age": 30}
        self.helper.insert(self.collection_name, document)
        inserted_doc = self.helper.db[self.collection_name].find_one({"name": "Alice"})
        self.assertIsNotNone(inserted_doc)
        self.assertEqual(inserted_doc['name'], "Alice")

    def test_find(self):
        document = {"name": "Alice", "age": 30}
        self.helper.db[self.collection_name].insert_one(document)
        results = self.helper.find(self.collection_name, {"name": "Alice"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Alice")

    def test_update(self):
        self.helper.db[self.collection_name].insert_one({"name": "Alice", "age": 30})
        self.helper.update(self.collection_name, {"name": "Alice"}, {"age": 31})
        updated_doc = self.helper.db[self.collection_name].find_one({"name": "Alice"})
        self.assertIsNotNone(updated_doc)
        self.assertEqual(updated_doc['age'], 31)

    def test_delete(self):
        self.helper.db[self.collection_name].insert_one({"name": "Alice", "age": 30})
        self.helper.delete(self.collection_name, {"name": "Alice"})
        deleted_doc = self.helper.db[self.collection_name].find_one({"name": "Alice"})
        self.assertIsNone(deleted_doc)

if __name__ == '__main__':
    unittest.main()