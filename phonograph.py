import credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import spotipy
import os
import sys
import json
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

def get_albums_from_spreadsheet():
  scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
  ]

  credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
  gc = gspread.authorize(credentials)
  wks = gc.open('Records').sheet1
  spreadsheet_albums = wks.get_all_records()

  username = sys.argv[1]
  spotifyObject = spotipy.Spotify(auth=get_spotify_token(username))

  bad = 0
  for spreadsheet_album in spreadsheet_albums:
    spotify_results = spotifyObject.search(q='artist:' + spreadsheet_album['Artist'] + ':album:' + spreadsheet_album['Album'], type='album')
    if len(spotify_results['albums']['items']) == 0:
      print('*** ' + spreadsheet_album['Artist'] + ': ' + spreadsheet_album['Album'])
      bad += 1
    # else:
      # spotify_album = spotify_results['albums']['items'][0]
      # print(spreadsheet_album['Artist'] + ': ' + spreadsheet_album['Album'] + ' : ' + spotify_album['release_date'])
  print(str(bad) + ' bad')
  return spreadsheet_albums

def prompt_for_token(username):
  spotify_scope = 'user-library-read'
  return util.prompt_for_user_token(username, spotify_scope, client_id=credentials.spotify['client_id'],client_secret=credentials.spotify['client_secret'],redirect_uri=credentials.spotify['redirect_uri'])

def get_spotify_token(username):
  try:
    token = prompt_for_token(username)
  except:
    os.remove(f".cache-{username}")
    token = prompt_for_token(username)

  return token

get_albums_from_spreadsheet()
