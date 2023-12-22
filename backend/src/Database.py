from pymongo import MongoClient

# mock_db = False
# if mock_db:
#     from mongomock import MongoClient as MockMongoClient
#     self.client = MockMongoClient()
# else:
#     with open(
#             os.path.join(os.path.dirname(__file__), '..', 'tmp',
#                             'key.json')) as f:
#         key_json = json.load(f)
#     mg_password = key_json["mongodb"]
#     uri = f"mongodb+srv://master:{mg_password}@cluster0.7pgqvs4.mongodb.net/?retryWrites=true&w=majority"
#     self.client = MongoClient(uri, server_api=ServerApi('1'))

# try:
#     self.client.admin.command('ping')
#     print(
#         "Pinged your deployment. You successfully connected to MongoDB!"
#     )