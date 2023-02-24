#モジュールをインポート(モジュールが分からなかったら調べてください)
import os
import logging
from flask import Flask, request, abort

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, PostbackAction, FollowEvent
)

app = Flask(__name__)

#LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKENは個人のチャンネルシークレットとチャンネルアクセストークンをexport
#export LINE_CHANNEL_SECRET=【シークレットチャンネルキー】,  export LINE_CHANNEL_ACCESS_TOKEN= 【チャンネルアクセストークン】
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

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
@handler.add(FollowEvent)
def follow_message(line_follow_event):
        profile = line_bot_api.get_profile(line_follow_event.source.user_id)
        logger.info(profile)
        line_bot_api.reply_message(line_follow_event.reply_token, TextSendMessage(text=f'{profile.display_name}さん、フォローありがとう!レシピと入力すると選択肢が現れるよ！！\n'))
@handler.add(MessageEvent, message=TextMessage)
# ここから実装開始
def handle_message(line_reply_event):
    profile = line_bot_api.get_profile(line_reply_event.source.user_id)
    logger.info(profile)
    message = line_reply_event.message.text.lower()
    if message == 'レシピ':
        line_bot_api.reply_message(line_reply_event.reply_token,TextSendMessage(text='このレシピでいいですか',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=PostbackAction(label="〇", data="〇", text="〇")),
                                QuickReplyButton(action=PostbackAction(label="×", data="×", text="×")),
                            ])
                    ))
if __name__ == "__main__":
    app.run()