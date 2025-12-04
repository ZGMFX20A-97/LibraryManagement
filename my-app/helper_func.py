from http import client
from google_client import GoogleClient
import os
from dotenv import load_dotenv
import re
import datetime


load_dotenv()
SS_ID = os.environ.get('SPREAD_SHEET_ID')

client = GoogleClient()
worksheet = client.get_sheet(SS_ID)

def get_books(keyword:str):
    book_records = worksheet.get_all_values()
    safe_keyword = re.escape(keyword) if keyword else ""
    books = []

    for book_record in book_records[1:]:
        book_title = book_record[2]
        status = book_record[3]

        # 3. 条件チェック
        # (A) キーワードが含まれている (大文字小文字無視)
        # (B) かつ、ステータスが「書架」である
        if re.search(safe_keyword, book_title, re.IGNORECASE) and status == "書架":
            books.append({
                "book_title": book_title,
                "status": status
            })
    return books

def search(keyword:str):
    targets_raw = get_books(keyword)

    targets = targets_raw.map(lambda t:{
                "text": {"type": "plain_text", "text": t.book_title},
                "value": t.book_title
        })

    return targets

def is_borrow_date_ok(input_date):

    selected_date = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()
    today = datetime.date.today()

    return selected_date >= today

def borrow(book,borrow_date):
    book_records = worksheet.get_all_values()
    cell = worksheet.find(book, in_column=3)


# class Book:
#     def __init__(self,arrangement_date,publisher,name):
#         self.arrangement_date = arrangement_date
#         self.publisher = publisher
#         self.name = name
