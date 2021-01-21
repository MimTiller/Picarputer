import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID="c04a53506ea54cc3b46cb7fdf0deffde"
SPOTIPY_CLIENT_SECRET= "404d47507d8c4c899a1fee325dd17a61"
scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-recently-played user-read-currently-playing'
username='subcake'
redirect = 'http://example.com'

def session_cache():
	cache_file = os.getcwd()+"\\.cache-{}".format(username)
	return(cache_file)

def login():
	global sp
	global token
	try:
		auth_manager=SpotifyOAuth(username=username,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=redirect)
		sp = spotipy.Spotify(auth_manager=auth_manager)

		print("(spotify.py): Logging in...")
		user = sp.me()['id']
		print("(spotify.py) logged in as {}".format(user))

	except Exception as e:
		print("spotify exception:")
		print(e)

def reauth():
	global sp
	global token
	try:
		auth_manager=SpotifyOAuth(username=username,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=redirect)
		sp = spotipy.Spotify(auth_manager=auth_manager)

		print("(spotify.py): Logging in...")
		user = sp.me()['id']
		print("(spotify.py) logged in as {}".format(user))
		return(sp)
	except Exception as e:
		print("spotify exception:")
		print(e)
def get_playing():
	global sp
	song = {}
	cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache())
	auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
		print("token not validated! trying to reauthenticate")
		sp = reauth()

	try:
		playing = sp.current_playback()

		if playing == None:
			print("get_playing: couldnt find current_playback(), trying current_user_playing_track()")
			playing = sp.current_user_playing_track()
		print("get_playing:",playing)
		if playing['currently_playing_type'] == 'episode':
			print("its a podcast!")
			song['artist'] = playing['item']['show']['name']
			song['album'] = ''
			song['track'] = playing['item']['name']
			song['art'] = playing['item']['images'][0]['url']
			song['type'] = "podcast"
			song['position'] = playing['progress_ms']
			song['duration'] = playing['item']['duration_ms']
		else:
			song['artist'] = playing['item']['artists'][0]['name']
			song['album'] = playing['item']['album']['name']
			song['track'] = playing['item']['name']
			song['art'] = playing['item']['album']['images'][0]['url']
			song['images']=playing['item']['album']['images']
			song['type'] = "song"
			song['position'] = playing['progress_ms']
			song['duration'] = playing['item']['duration_ms']
			song['is_playing'] = playing['is_playing']
			song['shuffle_state'] = playing ['shuffle_state']
		return (song)
	except Exception as e:
		print("spotify Exception")
		print(e)
		sp = reauth()
		pass


		#print('(spotify.py) re-authenticating')
		#auth = reauth()
		#playing = sp.current_playback(additional_types='episode')


def search(search_terms):
	global sp
	search = sp.search(search_terms,type='track,artist',limit=1)
	return(search)

def control(command):
	global sp
	try:
		if command == 'next':
			sp.next_track()
		elif command == 'previous':
			sp.previous_track()
		elif command == 'play':
			sp.start_playback()
		elif command == 'pause':
			sp.pause_playback()
		elif command == 'shuffle_on':
			sp.shuffle(True)
		elif command == 'shuffle_off':
			sp.shuffle(False)
		if isinstance(command,int):
			sp.volume(command)
	except spotipy.exceptions.SpotifyException as e:
		print(e)
login()
