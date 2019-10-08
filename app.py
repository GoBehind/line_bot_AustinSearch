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

app = Flask(__name__)

line_bot_api = LineBotApi('/PT8n0GdwXKZGZ+5RStOYF5+Q7KUT3psTYWpBvH9Pzan3mL1HA1dGNG7nEcNUh3nGkccI7uNZcyl+Nucfy7o+CPTQ6nCtS33Z8S/a4BxiM6xJ4fP4RABqOtJlgYeJwQfeXzRoZZEbIYp8xRThdpVGwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9354d812fc706d0790a89721d1552345')

liss = []
p = 0

while p < 34:
    p = p + 1
    url = 'https://www.austin.com.tw/products.php?func=p_list&pc_parent=0&nowp=' + str(p)

    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html5lib')
        
    goods = soup.find_all('div', 'info')
        

    for good in goods:
        title = good.find('span', 'product-brand').text.strip()
        product_name = good.find('span', 'product-type').text.strip()
        price = good.find('span', 'product-price sale').text.strip()
        lis = (title, product_name, price)

        liss.append(lis)

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