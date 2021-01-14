import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time



global sp
SPOTIPY_CLIENT_ID="c04a53506ea54cc3b46cb7fdf0deffde"
SPOTIPY_CLIENT_SECRET= "404d47507d8c4c899a1fee325dd17a61"
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
username='subcake'

def session_cache():
	cache_file = os.getcwd()+"\\.cache-{}".format(username)
	print(cache_file)
	return(cache_file)


auth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri="https://google.com",cache_path=session_cache())
try:
    #token = util.prompt_for_user_token(username, scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri="https://google.com",cache_path=session_cache())
	pass
except (AttributeError, JSONDecodeError) as e:
	print(e)
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)

print("(spotify.py): Logging in...")
sp = spotipy.Spotify(auth_manager=auth)
user = sp.me()['id']
print("(spotify.py) logged in as {}".format(user))
devices = sp.devices()
#print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']


device_list = []
for x in devices['devices']:
	device_list.append(x['name'])
print ("(spotify.py) Usable Devices: {}".format(device_list))


def reauth():
	sp = spotipy.Spotify(auth_manager=auth)
	print('(spotify.py) finished re-authenticating',sp)
	return(sp)

def get_playing():
	song = {}
	try:
		playing = sp.current_playback(additional_types='episode')

	except spotipy.client.SpotifyException:
		print('(spotify.py) re-authenticating')
		auth = reauth()
		playing = auth.current_playback(additional_types='episode')

	if not playing:
		print("(spotify.py) nothing playing")
		pass
	if playing != None:
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

def search(search_terms):
	search = sp.search(search_terms,type='track,artist',limit=1)
	return(search)

def control(command):
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
