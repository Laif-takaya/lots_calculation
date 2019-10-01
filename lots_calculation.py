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
YOUR_CHANNEL_ACCESS_TOKEN = "KMVTxjxp7pxbUHk9Xb4uL0v8/1rDvOJUOfAR5tp18ImgWBJn349FApfcqyR2xmStAYoabAyfTpcAv5AyJAF0Fq+sFJKddUVgPo+cSbXk3YucNLlYHXEt+wd+0BngdGyWcKUXMXkDcjYFDWYS9J1zfAdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "51eaf0af063d62d67140f01297f1b310"

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

    currency_pair=req_message[:7]
    stop=req_message[0:2]
    up_down=req_message[-2:]
    if currency_pair=="USD/JPY":
          a="ドル円"
    elif currency_pair=="EUR/JPY":
          a="ユーロ円"
    elif currency_pair=="EUR/USD":
          a="ユーロドル"
    elif currency_pair=="AUD/JPY":
          a="豪円"
    elif currency_pair=="AUD/USD":
          a="豪ドル"
    elif currency_pair=="GBP/JPY":
          a="ポンド円"
    elif currency_pair=="NZD/JPY":
          a="ニュージランド円"
    else:
          a="通過ペアは存在しません"

    if up_down=="ハイ":
          c="上"
    elif up_down=="ロー":
          c="下"
    else:
          c="不明"

    text_back=a+c
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text_back))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
