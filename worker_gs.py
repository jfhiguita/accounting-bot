import gspread, pandas

from settings import SPREAD_SHEET_KEY


class GsheetWorker:
    def __init__(self):
        self.gc = gspread.service_account(filename='googledrive_credentials.json')
        self.sh = self.gc.open_by_key(SPREAD_SHEET_KEY)


    def open_sheet(self, sheet_name):
        sheet = self.sh.worksheet(sheet_name)

        return sheet

if __name__ == "__main__":
    gsconn = GsheetWorker()
    print(gsconn.open_sheet("BALANCE"))