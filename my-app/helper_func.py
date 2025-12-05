from http import client
from google_client import GoogleClient
import os
from dotenv import load_dotenv
import re
import datetime
import gspread
from view import build_borrow_successful_block,build_return_successful_block

load_dotenv()
SS_ID = os.environ.get('SPREAD_SHEET_ID')

client = GoogleClient()
worksheet = client.get_sheet(SS_ID)


def get_books_can_be_borrowed(keyword:str):
    book_records = worksheet.get_all_values()
    safe_keyword = re.escape(keyword) if keyword else ""
    books = []

    for row,book_record in enumerate(book_records[1:], 2):
        book_title = book_record[2]
        status = book_record[3]

        # 3. 条件チェック
        # (A) キーワードが含まれている (大文字小文字無視)
        # (B) かつ、ステータスが「書架」である
        if re.search(safe_keyword, book_title, re.IGNORECASE) and status == "書架":
            books.append({
                "row": row,
                "book_title": book_title,
            })
    return books


def get_books_can_be_returned(user_name:str):
    book_records = worksheet.get_all_values()
    books = []

    for row,book_record in enumerate(book_records[1:], 2):
        user_name_from_sheet = book_record[4]
        status = book_record[3]
        book_title=book_record[2]

        # 3. 条件チェック
        # ユーザーネームが含まれている (大文字小文字無視)
        if re.search(user_name, user_name_from_sheet, re.IGNORECASE)and status == "貸出中":
            books.append({
                "row": row,
                "book_title": book_title,
            })

    return books


def search(keyword:str):
    targets_raw = get_books_can_be_borrowed(keyword)

    targets = list(map(lambda t:{
                "text": {"type": "plain_text", "text": t["book_title"]},
                "value": t["book_title"]
        },targets_raw))

    return targets


def is_borrow_date_ok(input_date):

    selected_date = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()
    today = datetime.date.today()

    return selected_date >= today


def borrow_book(book_title:str,user_name:str,return_date:str):
    book_records = get_books_can_be_borrowed(book_title)

    if len(book_records) == 0:
        raise gspread.exceptions.GSpreadException
    target_row = book_records[0]["row"]

    today_formatted = datetime.date.today().strftime('%Y/%m/%d')
    return_date_formatted = return_date.replace("-","/")

    update_values = [["貸出中", user_name, today_formatted, return_date_formatted]]

    try:
        worksheet.update(range_name=f"D{target_row}:G{target_row}", values=update_values,value_input_option="USER_ENTERED")
        return build_borrow_successful_block(book_title,user_name,today_formatted,return_date_formatted)
    except gspread.exceptions.GSpreadException:
        raise


def return_book(book_title:str,user_name:str):
    book_records = get_books_can_be_returned(user_name)
    today_formatted = datetime.date.today().strftime('%Y/%m/%d')
    update_values = [["書架", "", "", ""]]
    target_row = None

    if len(book_records) == 0:
        raise gspread.exceptions.GSpreadException

    for book_record in book_records:
        if re.search(book_title,book_record["book_title"], re.IGNORECASE):
            target_row = book_record["row"]

    try:
        worksheet.update(range_name=f"D{target_row}:G{target_row}", values=update_values,value_input_option="USER_ENTERED")
        return build_return_successful_block(book_title,user_name,today_formatted)
    except gspread.exceptions.GSpreadException:
        raise


def clean_name(display_name: str) -> str:
    # 正規表現で不要な文字を空文字に置換する
    # [a-zA-Z] : アルファベット全て
    # \s       : 空白（スペース）
    cleaned_name = re.sub(r'[a-zA-Z\s]', '', display_name)

    return cleaned_name
