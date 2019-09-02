from google_sheet import GoogleSheet
from spotify import Spotify

sheet_records = GoogleSheet().records()

spotify = Spotify()
spotify.print_albums(sheet_records)