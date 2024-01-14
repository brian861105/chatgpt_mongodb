import os

channel_secret = os.getenv('LineBotChannelSecret')
channel_access_token = os.getenv('LineBotToken')

target_api_url = os.getenv('FLASK_API_URL')
from flask import Flask, request, abort, Blueprint
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

line_bot_blueprint = Blueprint('/linebot', __name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@line_bot_blueprint.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    payload = {'text', message_text}
    response = requests.post(target_api_url, json=payload)
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=response))


@handler.default()
def default(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text="請使用文字訊息回覆，謝謝！"))
