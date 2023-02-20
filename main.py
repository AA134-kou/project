#モジュールをインポート(モジュールが分からなかったら調べてください)
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

#LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKENは個人のチャンネルシークレットとチャンネルアクセストークンをexport
#export LINE_CHANNEL_SECRET=【シークレットチャンネルキー】,  export LINE_CHANNEL_ACCESS_TOKEN= 【チャンネルアクセストークン】
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
#この関数は、LINE Bot API 経由で入力テキストを処理します。
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
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