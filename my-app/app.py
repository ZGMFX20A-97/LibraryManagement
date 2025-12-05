import logging
import os
from helper_func import borrow_book,return_book,search,is_borrow_date_ok,clean_name,get_books_can_be_returned
from dotenv import load_dotenv
from view import build_borrow_view,build_return_view
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
logging.basicConfig(level=logging.DEBUG)
load_dotenv()


@app.command("/lib")
def handle_command(ack, body, client):
    ack()

    text = body.get("text", "").strip()
    channel_id = body["channel_id"]
    user_id = body["user_id"]
    response = client.users_info(user=user_id)
    user_name = clean_name(str(response["user"]["profile"]["real_name"]))

    if text == "borrow":
        borrow_modal_view = build_borrow_view(channel_id)
        # 貸出用モーダルを開く
        client.views_open(trigger_id=body["trigger_id"],view=borrow_modal_view)
    elif text == "return":
        books_can_be_returned = get_books_can_be_returned(user_name)
        # 返却用モーダルを開く
        return_modal_view = build_return_view(user_name,channel_id,books_can_be_returned)
        client.views_open(trigger_id=body["trigger_id"],view=return_modal_view)


@app.options("borrow_select")
def show_books_options(ack,payload):
    keyword = str(payload.get("value"))
    options = search(keyword)

    ack(options=options)


@app.view("borrow_modal",)
def handle_borrow(ack,body,view,client):
    # 1. リクエストボディからデータの取得
    selected_date = str(view['state']['values']['date_block']['date_select']['selected_date'])
    user_id = body["user"]["id"]
    book_data = str(view['state']['values']['book_block']['borrow_select']['selected_option']['value'])
    channel_id = str(view["private_metadata"])
    response = client.users_info(user=user_id)
    user_name = clean_name(str(response["user"]["profile"]["real_name"]))

    # 2. 日付の比較ロジック
    date_ok = is_borrow_date_ok(selected_date)
    if not date_ok:
        # 入力された日付が今日より前（過去）の場合
        ack(
            response_action="errors",
            errors={
                "date_block": "過去の日付は選択できません。今日以降の日付にしてください。"
            }
            )
        return
    else:
        try:
            block = borrow_book(book_data,user_name,selected_date)
            app.client.chat_postMessage(channel=channel_id,blocks=block)
            ack()
        except:
            app.client.chat_postMessage(text="シート更新にエラーが発生しました。シートを整理してください",channel=channel_id)
            ack()


@app.view("return_modal")
def handle_return(ack,body,view,client):
    user_id = body["user"]["id"]
    response = client.users_info(user=user_id)
    user_name = clean_name(str(response["user"]["profile"]["real_name"]))
    book_data = str(view['state']['values']['book_block']['return_select']['selected_option']['value'])
    channel_id = str(view["private_metadata"])

    try:
        block = return_book(book_data,user_name)
        app.client.chat_postMessage(channel=channel_id,blocks=block)
        ack()
    except:
        app.client.chat_postMessage(text="シート更新にエラーが発生しました。シートを整理してください",channel=channel_id)
        ack()



if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
