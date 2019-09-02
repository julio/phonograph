import credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import spotipy
import os
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

def get_albums_from_google_sheet():
  scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
  ]

  google_credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
  gc = gspread.authorize(google_credentials)
  wks = gc.open('Records').sheet1

  return wks.get_all_records()

def print_albums_from_spotify(spreadsheet_albums):
  username = credentials.spotify['username']
  spotifyObject = spotipy.Spotify(auth=get_spotify_token(username))

  bad = 0
  for spreadsheet_album in spreadsheet_albums:
    spotify_results = spotifyObject.search(q='artist:' + spreadsheet_album['Artist'] +
      ':album:' + spreadsheet_album['Album'],
      type='album')
    if len(spotify_results['albums']['items']) == 0:
      print('*** ' + spreadsheet_album['Artist'] + ': ' + spreadsheet_album['Album'])
      bad += 1
    else:
      spotify_album = spotify_results['albums']['items'][0]
      print(spreadsheet_album['Artist'] + ': ' +
        spreadsheet_album['Album'] + ' : ' +
        spotify_album['release_date'])
  print(str(bad) + ' bad')

def get_albums():
  spreadsheet_albums = get_albums_from_google_sheet()

  print_albums_from_spotify(spreadsheet_albums)

def prompt_for_token(username):
  spotify_scope = 'user-library-read'
  return util.prompt_for_user_token(username, spotify_scope,
    client_id=credentials.spotify['client_id'],
    client_secret=credentials.spotify['client_secret'],
    redirect_uri=credentials.spotify['redirect_uri'])

def get_spotify_token(username):
  try:
    token = prompt_for_token(username)
  except:
    os.remove(f".cache-{username}")
    token = prompt_for_token(username)

  return token

get_albums()
