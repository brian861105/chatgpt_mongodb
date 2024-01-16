import os
import requests
channel_secret = os.getenv('LineBotChannelSecret')
channel_access_token = os.getenv('LineBotToken')
target_api_url = "http://0.0.0.0:80/linebot_receive_message"

from flask import Flask, request, abort, Blueprint, current_app

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


line_bot_blueprint = Blueprint('linebot', __name__)
@line_bot_blueprint.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        error_msg = "Invalid signature. Please check your channel access token/channel secret."
        current_app.logger.info(error_msg)
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_id = event.source.user_id
        client_text = event.message.text
        data = {
            "user_id": user_id,
            "role" : "assistant",
            "content": client_text
        }
        url = target_api_url
        response = requests.post(url, json=data)
        response = response.json()
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response["content"])]
            )
        )

@handler.default()
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        response = "請使用文字訊息詢問！"
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )
