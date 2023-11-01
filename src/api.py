from flask import Flask, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def test_route():
    return jsonify({'msg': 'you are amazing!'})