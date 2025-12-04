borrow_modal_view= {
	"title": {
		"type": "plain_text",
		"text": "書籍の貸出"
	},
	"submit": {
		"type": "plain_text",
		"text": "貸出"
	},
	"type": "modal",
	"callback_id": "borrow_modal",
	"close": {
		"type": "plain_text",
		"text": "キャンセル"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "book_block",
      "optional": False,
			"label": {
				"type": "plain_text",
				"text": "書籍を検索"
			},
			"element": {
				"type": "external_select",
				"action_id": "book_select",
				"placeholder": {
					"type": "plain_text",
					"text": "書籍名を検索..."
				},
				"min_query_length": 1
			}
		},
		{
			"type": "input",
			"block_id": "date_block",
			"optional": False,
			"label": {
				"type": "plain_text",
				"text": "返却予定日"
			},
			"element": {
				"type": "datepicker",
				"action_id": "date_select",
				"placeholder": {
					"type": "plain_text",
					"text": "日付を選択"
				}
			}
		}
	]
}

return_modal_view={
	"title": {
		"type": "plain_text",
		"text": "書籍の返却"
	},
	"submit": {
		"type": "plain_text",
		"text": "返却"
	},
	"type": "modal",
	"callback_id": "return_modal",
	"close": {
		"type": "plain_text",
		"text": "キャンセル"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "book_block",
      "optional": False,
			"label": {
				"type": "plain_text",
				"text": "書籍を検索"
			},
			"element": {
				"type": "external_select",
				"action_id": "book_select",
				"placeholder": {
					"type": "plain_text",
					"text": "書籍名を検索..."
				},
				"min_query_length": 1
			}
		}
	]
}
