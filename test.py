from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def post(self):
        # 取得 POST 請求中的資料
        user_name = request.json.get('user_name')  # 假設 JSON 數據中有 'user_name' 欄位
        print(user_name)

        # 執行您的邏輯（這裡僅打印用戶名）
        print(f"Received user name: {user_name}")

        # 回應
        return {'message': 'User created successfully'}, 201  # 201 表示成功建立資源

api.add_resource(User, '/users')

if __name__ == '__main__':
    app.run(debug=True)