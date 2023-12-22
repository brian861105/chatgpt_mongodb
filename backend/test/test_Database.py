# test_database.py
import pytest
from pymongo import MongoClient
from config.config import MONGODB_URI
from src.Database import DatabaseManager

@pytest.fixture
def mongo_client():
    client = MongoClient(MONGODB_URI)
    yield client
    client.close()

def test_connect_to_mongodb(mongo_client):
    db = mongo_client.get_database('my_database')
    assert mongo_client.is_primary

def test_database_manager_with_mock():
    database_manager = DatabaseManager(mock_db=True, simulate_connection_failure=False)
    assert database_manager.is_connect() == True

def test_database_manager_with_mock_fail():

    database_manager_failure = DatabaseManager(mock_db=True, simulate_connection_failure=True)
    assert database_manager_failure.is_connect() == False

def test_create_database():
    database_manager = DatabaseManager(mock_db=True, simulate_connection_failure=False)
    collection_name = "test_collection"
    assert database_manager.create_collection(collection_name) == True

# def test_create_collection_already_exists():
#     database_manager = DatabaseManager(mock_db=True, simulate_connection_failure=False)
#     assert database_manager.is_connect() == True

#     collection_name = "test_collection"
#     assert database_manager.create_collection(collection_name) == True

#     assert database_manager.create_collection(collection_name) == False
# def test_read_database():

# def test_update_database():

# def test_delete_database():

# def test_database_is_primary():
#     database_manager = DatabaseManager(mock_db=False)