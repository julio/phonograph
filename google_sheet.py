from oauth2client.service_account import ServiceAccountCredentials
import gspread

class GoogleSheet:
  def __init__(self):
    self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    google_credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', self.scope)

    self.gc = gspread.authorize(google_credentials)
    self.wks = self.gc.open('Records').sheet1

  def records(self):
    return self.wks.get_all_records()
