import gspread, pandas as pd

from settings import SPREAD_SHEET_KEY

SHEET = "BALANCE"

class GsheetWorker:
    def __init__(self):
        self.gc = gspread.service_account(filename='googledrive_credentials.json')
        self.sh = self.gc.open_by_key(SPREAD_SHEET_KEY)


    def open_sheet(self, sheet_name):
        sheet = self.sh.worksheet(sheet_name)

        return sheet


    def check_items(self):
        sheet = self.open_sheet('BALANCE')
        items = pd.DataFrame(sheet.get_all_records())

        return items


    def storage_register(self, user_data):
        sheet = self.open_sheet(SHEET)
        if user_data:
            sheet.append_row([value for value in user_data.values()])
            notify = "La informacion ha sido registrada!"
        else:
            notify = "No hay data para guardar."

        return notify


if __name__ == "__main__":

    print(GsheetWorker().check_items())