from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


from bs4 import BeautifulSoup

import requests

app = Flask(__name__)

line_bot_api = LineBotApi('/PT8n0GdwXKZGZ+5RStOYF5+Q7KUT3psTYWpBvH9Pzan3mL1HA1dGNG7nEcNUh3nGkccI7uNZcyl+Nucfy7o+CPTQ6nCtS33Z8S/a4BxiM6xJ4fP4RABqOtJlgYeJwQfeXzRoZZEbIYp8xRThdpVGwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9354d812fc706d0790a89721d1552345')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()