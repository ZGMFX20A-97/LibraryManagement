def build_borrow_view(channel_id):
    return {
        "title": {
            "type": "plain_text",
            "text": "書籍の貸出",
        },
        "private_metadata": channel_id,
        "submit": {
            "type": "plain_text",
            "text": "貸出",
        },
        "type": "modal",
        "callback_id": "borrow_modal",
        "close": {
            "type": "plain_text",
            "text": "キャンセル",
        },
        "blocks": [
            {
                "type": "input",
                "block_id": "book_block",
                "optional": False,
                "label": {
                    "type": "plain_text",
                    "text": "書籍を検索",
                },
                "element": {
                    "type": "external_select",
                    "action_id": "borrow_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "書籍名を検索...",
                    },
                    "min_query_length": 1,
                },
            },
            {
                "type": "input",
                "block_id": "date_block",
                "optional": False,
                "label": {
                    "type": "plain_text",
                    "text": "返却予定日",
                },
                "element": {
                    "type": "datepicker",
                    "action_id": "date_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "日付を選択",
                    },
                },
            },
        ],
    }


def build_return_view(user_name, channel_id,books_can_be_returned):

    view = {
        "type": "modal",
        "callback_id": "return_modal",
        "private_metadata": channel_id,
        "title": {"type": "plain_text", "text": "書籍の返却"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [],  # ここにブロックを追加していく
    }

    if not books_can_be_returned:
        view["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📚 *{user_name}* さんが現在借りている書籍はありません。",
                },
            }
        )
    else:
        # プルダウンの選択肢を作成
        options = [
            {
                "text": {"type": "plain_text", "text": book["book_title"]},
                "value": book["book_title"],
            }
            for book in books_can_be_returned
        ]

        view["blocks"].append(
            {
                "type": "input",
                "block_id": "book_block",
                "label": {"type": "plain_text", "text": "返却する書籍を選択"},
                "element": {
                    "type": "static_select",
                    "action_id": "return_select",
                    "placeholder": {"type": "plain_text", "text": "書籍を選択"},
                    "options": options,  # ★ここが1件以上あることが保証される
                },
            }
        )
        view["submit"] = {"type": "plain_text", "text": "返却"}

    return view


def build_borrow_successful_block(book_title,user_name,today,return_date):

	return [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "📚 書籍の貸出完了",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*書籍名:*\n{book_title}"
				},
				{
					"type": "mrkdwn",
					"text": f"*借りた人:*\n{user_name}"
				},
				{
					"type": "mrkdwn",
					"text": f"*貸出日:*\n{today}"
				},
				{
					"type": "mrkdwn",
					"text": f"*返却予定日:*\n{return_date}"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "⚠️ 読み終わったら早めに返却してくださいね"
				}
			]
		}
	]


def build_return_successful_block(book_title,user_name,today):

	return [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "📚 書籍の返却完了",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*書籍名:*\n{book_title}"
				},
				{
					"type": "mrkdwn",
					"text": f"*借りた人:*\n{user_name}"
				},
				{
					"type": "mrkdwn",
					"text": f"*返却日:*\n{today}"
				}
			]
		}
	]
