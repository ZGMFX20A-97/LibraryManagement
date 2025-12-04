import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleClient():
    def __init__(self):
        self.client = gspread.service_account(filename="secretkey.json")

    def get_sheet(self,spreadsheet_id):
        spreadsheet = self.client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.get_worksheet(0)

        return worksheet
