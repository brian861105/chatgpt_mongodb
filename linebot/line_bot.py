import os

channel_secret = os.getenv('CHANNEL_SECRET')
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定 Channel Access Token 與 Channel Secret
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # signature = request.headers['X-Line-Signature']
    # body = request.get_data(as_text=True)

    try:
        data = request.json
        # print(data)
        print(data["events"][0]["message"]["text"])
        # handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_text = f"You said: {message_text}"
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run(port=6000)
