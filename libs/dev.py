SPOTIPY_CLIENT_ID="c04a53506ea54cc3b46cb7fdf0deffde"
SPOTIPY_CLIENT_SECRET= "404d47507d8c4c899a1fee325dd17a61"
scope = 'user-read-private user-read-playback-state user-modify-playback-state '
redirect = 'https://google.com'
username='subcake'

import spotipy
import spotipy.util as util

from pprint import pprint

while True:
    username = input("Type the Spotify user ID to use: ")
    token = util.prompt_for_user_token(username, show_dialog=True,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=redirect)
    sp = spotipy.Spotify(token)
    print(sp.me())
