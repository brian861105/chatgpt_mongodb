from flask import Flask, jsonify
from markupsafe import escape
import api
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

SERVER_PORT = 3000
SERVER_HOST = "127.0.0.1"
password = "WyJRepqRLIZ7K5CJ"
uri = f"mongodb+srv://master:{password}@cluster0.7pgqvs4.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['mydatabase']
collection = db['users']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def show_run():
    print(f"Server is running on http://{SERVER_HOST}:{SERVER_PORT}")

app = Flask(__name__)
@app.route('/')
def index():
    return 'Index Page'

app.add_url_rule('/test/', view_func=api.test_route, methods=['GET'])

# capture all the error process
@app.errorhandler(Exception)
def handle_error(error):
    status = getattr(error, 'code', 500) if isinstance(error, HTTPException) else 500

    if status == 500:
        print('The server errored when processing a request')
        print(error)

    response = {
        'status': status,
        'message': getattr(error, 'description', 'Internal Server Error')
    }
    return jsonify(response), status

# for 404 error
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Page did not exist'}), 404

if __name__ == '__main__':
    show_run()
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)