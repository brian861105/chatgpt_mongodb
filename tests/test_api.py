import os
import sys

from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from flask import Flask
from flask.testing import FlaskClient
from app.api import app
import pytest

@pytest.fixture
def client(request) -> FlaskClient:
    app.config['TESTING'] = True
    
    return app.test_client()
    

def test_create_user_session(client):
    data = {"user_name": "test_user"}
    response = client.post('/user', json=data)
    assert response.status_code == 201
    response_data = response.get_json()
    assert "sessionId" in response_data
    assert response_data["user"] == "test_user"

def test_create_user_session_empty_json(client):
    # 發送空的 JSON 數據的 POST 請求
    data = {"user_name": ""}
    response = client.post('/user', json=data, content_type='application/json')
    # 檢查回應的 HTTP 狀態碼是否為 400 或其他你期望的狀態碼
    assert response.status_code == 400
    
    # 檢查回應的 JSON 內容是否包含 "error" 鍵
    response_data = response.get_json()
    assert "error" in response_data
    
    # 檢查 "error" 鍵的值是否正確
    assert response_data["error"] == "User ID is required"

def test_create_user_session_no_json(client):
    # 發送完全沒有提供 JSON 數據的 POST 請求
    response = client.post('/user', content_type='application/json')
    # 檢查回應的 HTTP 狀態碼是否為 400 或其他你期望的狀態碼
    assert response.status_code == 400
    
    # 檢查回應的 JSON 內容是否包含 "error" 鍵
    response_data = response.get_json()
    assert "message" in response_data
    
    # 檢查 "error" 鍵的值是否正確
    assert response_data["message"] == 'The browser (or proxy) sent a request that this server could not understand.'


def test_get_user_sessions(client):
    response = client.get('/user/user_1/sessions')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
