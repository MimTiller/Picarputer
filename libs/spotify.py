import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time
from spotipy.oauth2 import SpotifyOAuth
import configparser
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp



class Spotify_ctrl():

	def __init__(self):
		self.config=configparser.ConfigParser()
		self.config.read('spotify.cfg')
		self.SPOTIPY_CLIENT_ID=self.config.get('SPOTIFY','CLIENT_ID')
		self.SPOTIPY_CLIENT_SECRET=self.config.get('SPOTIFY','CLIENT_SECRET')
		self.REDIRECT_URI=self.config.get('SPOTIFY','redirect')
		self.username=self.config.get('SPOTIFY','username')
		self.scope = 'user-read-private user-read-playback-state user-modify-playback-state user-read-recently-played user-read-currently-playing'

	def session_cache(self):
		cache_file = os.getcwd()+"\\.cache-{}".format(self.username)
		return(cache_file)

	def login(self):
		print("attempting login...")
		print("checking for cached token..({})".format(self.session_cache()))
		if os.path.exists(self.session_cache()):
			print("found token!")
			sp_oauth = SpotifyOAuth(
					scope=self.scope,
					client_id=self.SPOTIPY_CLIENT_ID,
					client_secret=self.SPOTIPY_CLIENT_SECRET,
					redirect_uri=self.REDIRECT_URI,
					cache_path=self.session_cache())
			#return the (sp) information to pass to other functions
			return spotipy.Spotify(auth_manager=sp_oauth)
		else:
			self.first_login()

			#util.py:82 oauth2.py:261
	def first_login(self):
		sp = self.sp
		sp_oauth = SpotifyOAuth(
				scope=scope,
				client_id=SPOTIPY_CLIENT_ID,
				client_secret=SPOTIPY_CLIENT_SECRET,
				redirect_uri=REDIRECT_URI,
				cache_path=session_cache())
		token_info = sp_oauth.get_cached_token()
		print("token info:" ,token_info)
		if not token_info:
			auth_url = sp_oauth.get_authorize_url()

		def _set_option(self,option):
			oauth_code_callback(option)
			self.popup.dismiss()

		def oauth_code_callback(code):
			try:
				token_info = sp_oauth.get_access_token(code)
				code = token_info['access_token']
				print(code)
				return code
			except Exception as e:
				print(e)
		def _input_popup(self,text):
			webbrowser.open(auth_url)
			content=BoxLayout(orientation='vertical')
			txt_input=TextInput(text=text)
			btnbox=BoxLayout()
			btn = Button(text = "OK")
			content.add_widget(txt_input)
			btnbox.add_widget(btn)
			content.add_widget(btnbox)
			popup_width = min(0.95 * Window.width, dp(300))
			popup_height = min(0.95 * Window.height, dp(400))
			self.popup = Popup(
			content=content, title='Spotify Login:', size_hint=(None, None),
			size=(popup_width, popup_height))
			btn.bind(on_release=lambda x:_set_option(self,txt_input.text))
			self.popup.open()
		_input_popup(self=App.get_running_app,text="open the URL in your browser and enter the code you recieved")


	def get_playing(self,sp):
		self.sp = sp
		song = {}
		playing = sp.current_playback()
		try:
			if playing == None:
				print("get_playing: couldnt find current_playback(), trying current_user_playing_track()")
				playing = sp.current_user_playing_track()
				print(playing)
			if playing['currently_playing_type'] == 'episode':
				playing = sp.current_playback(additional_types='episode')
				song['artist'] = playing['item']['show']['name']
				song['album'] = ''
				song['track'] = playing['item']['name']
				song['art'] = playing['item']['images'][0]['url']
				song['type'] = "podcast"
				song['position'] = playing['progress_ms']
				song['duration'] = playing['item']['duration_ms']
				song['is_playing'] = playing['is_playing']
				song['shuffle_state'] = playing ['shuffle_state']
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
			print(song)
		except Exception as e:
			print(e)


			#print('(spotify.py) re-authenticating')
			#auth = reauth()
			#playing = sp.current_playback(additional_types='episode')


	def search(search_terms):
		search = self.sp.search(search_terms,type='track,artist',limit=1)
		return(search)

	def control(command,sp):
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
