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
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "WS+Wolw2SG+oGZMBaJOOZyITQTNfi0321I+JHnZ0jeT/528+8do4AOtGjdvJyGL8vhIau7xlt0AtzJT0jVEuLhKDndFf+9kY23/yElYFd6aBKM3UoLu/Kt/iuB9qCb1Ho34idLyPDCBBsKELeqVirQdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "82870d88cfe62a8068a12b66ac294a6d"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    req_message=event.message.text

    #currency_pair=req_message[:7]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=req_message))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
