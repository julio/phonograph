import credentials
import spotipy
import spotipy.util as util
import os

class Spotify():
  def print_albums(self, spreadsheet_albums):
    username = credentials.spotify['username']
    spotifyObject = spotipy.Spotify(auth=self.get_spotify_token(username))

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

  def prompt_for_token(self, username):
    spotify_scope = 'user-library-read'
    return util.prompt_for_user_token(username, spotify_scope,
      client_id=credentials.spotify['client_id'],
      client_secret=credentials.spotify['client_secret'],
      redirect_uri=credentials.spotify['redirect_uri'])

  def get_spotify_token(self, username):
    try:
      token = prompt_for_token(username)
    except:
      os.remove(f".cache-{username}")
      token = self.prompt_for_token(username)

    return token
