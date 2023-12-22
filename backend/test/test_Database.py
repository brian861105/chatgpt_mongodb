# test_database.py
import pytest
from pymongo import MongoClient
from config.config import MONGODB_URI

@pytest.fixture
def mongo_client():
    client = MongoClient(MONGODB_URI)
    yield client
    client.close()

def test_connect_to_mongodb(mongo_client):
    db = mongo_client.get_database('my_database')
    assert mongo_client.is_primary
