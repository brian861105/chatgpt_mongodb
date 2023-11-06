from flask import Flask, jsonify, request, render_template, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os


# def chatgpt_get(user_id):
#     if(user_id not in ddd){
#         return {
#             "error" : "User ID is required"
#         }
#     }

# def chatgpt_post():
#     return "fuck2"

app = Flask(__name__)
@app.route('/login', methods=['GET', 'POST']) 
def login():
    # if request.method == 'POST': 
    #     return 'Hello ' + request.values['username'] 

    # return "<form method='post' action='/login'><input type='text' name='username' />" \
    #         "</br>" \
    #        "<button type='submit'>Submit</button></form>"
    if request.method == 'POST': 
        return 'Hello ' + request.values['username'] + \
                "</br>" \
                "<button type='submit'>Logout</button></form>"           

    return "<form method='post' action='/login'><input type='text' name='username' />" \
            "</br>" \
           "<button type='submit'>Submit</button></form>"

# if __name__ == '__main__':
#     app.debug = True
#     app.run()    

@app.route('/process_json', methods=['POST'])
def process_json():
    if request.method == 'POST':
        # 获取 JSON 数据
        # print("get data")
        # print(data)
        data = request.get_json()
        print(data)
        # data = jsonify(data)
        return render_template('display_json.html', data=data)
        # if data is not None:
        #     # 读取 JSON 数据中的特定键值对
        #     output = ""
        #     for key in data:
        #         value = data[key]
        #         output += f"{key} : {value} \n"
        #     # 在控制台打印读取的值
        #     print("Value from JSON:\n", output)
        #     # return output
        #     return "Received and processed JSON data."
        # else:
        #     return "No JSON data received."

if __name__ == '__main__':
    app.debug = True
    app.run()