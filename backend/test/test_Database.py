import pytest
from pymongo import MongoClient
from config.config import MongoURI
from src.Database import DatabaseManager
import json


def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


### With MockDB
@pytest.fixture
def mongo_client():
    client = MongoClient(MongoURI)
    yield client
    client.close()


def test_ConnectMongodb(mongo_client):
    db = mongo_client.get_database("my_database")
    assert mongo_client.is_primary


def test_CreateUserDatabaseWithMock():
    database_manager = DatabaseManager()
    UserId = "UserId"
    assert database_manager.CreateUser(UserId) == True


def test_ReadUserChatSession():
    database_manager = DatabaseManager()
    UserId = "UserId"
    assert is_valid_json(database_manager.ReadUser(UserId)) == True


def test_DeleteUserDatabase():
    database_manager = DatabaseManager()
    UserId = "UserId"
    assert database_manager.DeleteUser(UserId) == True


def test_CreateSessionDatabase():
    database_manager = DatabaseManager()
    UserId = "UserId"
    ResultData = database_manager.CreateSession(UserId)
    assert is_valid_json(ResultData) == True
    ResultData = json.loads(ResultData)
    assert isinstance(ResultData["SessionId"], str) == True


def test_DeleteSessionDatabase():
    database_manager = DatabaseManager()
    UserId = "UserId"
    CreateData = database_manager.CreateSession(UserId)
    CreateData = json.loads(CreateData)
    SessionId = CreateData["SessionId"]
    result = database_manager.DeleteSession(UserId, SessionId)
    assert result == True


# def test_RenameSessionTitle():
#     database_manager = DatabaseManager()
#     UserId = "UserId"
#     CreateData = database_manager.CreateSession(UserId)
#     CreateData = json.loads(CreateData)
#     SessionId = CreateData["SessionId"]
#     NewTitle = "hello world"
#     result = database_manager.RenameSessionTitle(UserId, SessionId, NewTitle)
#     assert result == True
