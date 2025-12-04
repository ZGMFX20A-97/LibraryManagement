import logging
import os
from helper_func import borrow, search,is_borrow_date_ok
from dotenv import load_dotenv
from view import borrow_modal_view,return_modal_view
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

@app.command("/lib")
def handle_command(ack, body, client):
    ack()
    text = body.get("text", "").strip()

    if text == "borrow":
        # 貸出用モーダルを開く
        client.views_open(trigger_id=body["trigger_id"],view=borrow_modal_view)
    elif text == "return":
        client.views_open(trigger_id=body["trigger_id"],view=return_modal_view)


@app.options("book_select")
def show_book_options(ack,payload):
    keyword = str(payload.get("value"))
    options = search(keyword)

    ack(options=options)

@app.view("borrow_modal",)
def handle_borrow(ack,view):
    # 1. 入力値の取得
    # view['state']['values'][block_id][action_id]['selected_date']
    # ※ block_id と action_id はご自身のコードに合わせて変更してください
    selected_date = view['state']['values']['date_block']['date_select']['selected_date']
    selected_date_str = str(selected_date)
        # 2. 日付の比較ロジック
    ok = is_borrow_date_ok(selected_date_str)

    if not ok:
        # 入力された日付が今日より前（過去）の場合
        ack(
            response_action="errors",
            errors={
                "date_block": "過去の日付は選択できません。今日以降の日付にしてください。"
            }
            )
    else:
        book_data = view['state']['values']['book_block']['book_select']['selected_option']['value']
        book_data_str = str(book_data)
        borrow(book_data_str,selected_date_str)


    # エラーがない場合は通常の処理を行い、ack()でモーダルを閉じる

        ack()

@app.view("return_modal",)
def handle_return(ack,view):
    pass




if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
