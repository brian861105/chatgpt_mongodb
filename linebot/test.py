from flask import Flask, request, abort

app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback():
    # 確認請求是否是 POST 請求
    if request.method == "POST":
        # 處理 LINE 平台發送的 Webhook 資料
        # 在這裡添加你的處理邏輯
        print(request.json)
        return "OK", 200
    else:
        # 如果不是 POST 請求，則回傳 404 Not Found
        abort(404)


if __name__ == "__main__":
    app.run(port=6000)
