 #!/usr/bin/python
#kivy imports
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.config import Config, ConfigParser
from kivy.clock import Clock

from kivy.garden.graph import MeshLinePlot, SmoothLinePlot
from kivy.garden.notification import Notification
from kivy.storage.jsonstore import JsonStore
from kivy.uix.settings import SettingsWithNoMenu, SettingOptions, SettingsWithSidebar, SettingItem
from kivy.metrics import dp
#layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

#widgets
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
#misc


from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition
from kivy.utils import get_color_from_hex as rgb
from kivy.graphics import *
#non kivy imports
from time import time
from random import shuffle
from multiprocessing import Process
import re, sys, os, random, threading, time, eyed3, mutagen, glob
import dataset, usb, psutil, importlib, json, concurrent.futures

from libs import tagger, audio, vlc, btdevices, initialize, settings
from libs.settings import SettingSlider, SettingDynamicOptions, MySettings
from threading import Thread
from collections import defaultdict
from os import path
from functools import partial

#==================CONFIGURATION========================================#
									    								#Force a resolution, or just comment out
screenupdatetime = 0.5													#how fast slider and song info updates. use lower values for faster time, but more cpu work
MusicDirectory="/home/subcake/Music"									#change what folder PiCarputer looks in for your music
#=======================================================================#


playicon = 'data/icons/play.png'
pauseicon = 'data/icons/pause.png'
db = dataset.connect('sqlite:///songlist.db')
table = db['songs']
settingsdb = db['settings']
global graph
#global wallpaper
graph = []






#-----------------------------#KIVY#------------------------------------
class ScreenManagement(ScreenManager):
    pass
class Menu(Screen):
	pass
class MusicScreen(Screen):
	pass
class SettingsScreen(Screen):
    pass
class OBDIIScreen(Screen):
	pass
class PerfScreen(Screen):
	pass
class Root(Screen):
	pass
class VolumeSlider(BoxLayout):
	pass
class PlayButtons(AnchorLayout):
	pass
class Scroller1(FloatLayout):
	pass
class Scroller2(FloatLayout):
	pass
class BigScreenInfo(BoxLayout):
	pass
class Notify(FloatLayout):
	pass

#get current screen resolution
x = initialize.current_res().split('x')
height = int(x[1])
width = int(x[0])
config = ConfigParser()
config.read('main.ini')
conf_res = config.get('General', 'resolutions').split('x')
confh = int(conf_res[1])
confw = int(conf_res[0])

#Set Resolution
Window.size = confw,confh
#Window.maximize()

#check Fullscreen
fs = config.get('General', 'fullscreen')
if fs == "1":
	Window.fullscreen = True
elif fs == "0":
	Window.fullscreen = False


class WallPaper(Image):
	wallpaper_selection = StringProperty()
	config = ConfigParser()
	config.read('main.ini')
	wallpaper = config.get('General', 'wallpaper')
	wpd = str('data/wallpapers/' + wallpaper)
	wallpaper_selection = wpd



#-----------------------MAIN-FUNCTIONS---------------------------------#
class MainThread(AnchorLayout):
	instance = vlc.Instance()
	player = instance.media_player_new("C:/test.wav")
	media = instance.media_new_path("unknown")
	player.set_media(media)
	player = vlc.MediaPlayer("/path/to/file.flac")



	def __init__(self, **kwargs):
		super(MainThread ,self).__init__(**kwargs)
		Clock.schedule_interval(self.refresh, screenupdatetime)
		Clock.schedule_once(self.start_thread,0)
		self.startupvolume = 75
		#self.buttonlist=[]
		#self.artistlist=[]
		#self.artistlistbool = False
		#self.level = "artist"
		self.notshuffled = []
		self.num = 0
		self.shuffle = True
		#self.dir_num = 13
		#self.artist_loaded = False
		self.artist = ''
		self.album = ''
		self.title = ''
		self.image = ''
		#self.splash = 1
		self.wallpaperlist = ListProperty()
		self.currentscreen = 1

	def hide_notify(self,widget,*args):
		notification = widget.root.ids.notify
		anim = Animation(pos_hint={'x':1},duration=.3)
		anim.start(notification)

	def notify(self,widget,title,message,timeout):
		notification = widget.root.ids.notify
		msg = widget.root.ids.notifymessage
		msg.text = str(message)
		ttl = widget.root.ids.notifytitle
		ttl.text = str(title)
		anim = Animation(pos_hint={'x':0.65},duration=.3)
		anim.start(notification)
		Clock.schedule_once(partial(self.hide_notify,self,widget),timeout)





	def slide_screen(self,instance,screenname):
		if instance > self.currentscreen:
			self.ids.st.transition = SlideTransition(direction="left")
			self.currentscreen = instance
		elif instance < self.currentscreen:
			self.ids.st.transition = SlideTransition(direction="right")
			self.currentscreen = instance
		else:
			pass
		self.ids.st.current = screenname



	def playpause(self):
		state = str(self.player.get_state())
		if state == "State.NothingSpecial":
			print ("[playpause] starting first time playback")
			self.ids.playpausebutton.source = playicon
			try:
				media = instance.media_new_path(self.next_Song)
				player.set_media(media)
				self.player.play()
			except:
				print ("error...couldnt play")
		elif state== "State.Playing":
			print ("[playpause] paused")
			self.ids.playpausebutton.source = playicon
			self.player.pause()
		elif state == "State.Paused":
			print ("[playpause] resuming")
			self.ids.playpausebutton.source = pauseicon
			self.player.play()

	def shuffleicon(self):
		shuffleon = 'data/icons/shuffle_on.png'
		shuffleoff = 'data/icons/shuffle.png'
		if self.shuffle == True:
			self.shuffle = False
			self.ids.shuffleimage.source=shuffleoff
			self.notshuffle = 0
			print ("Shuffle Off")
		elif self.shuffle == False:
			self.shuffle = True
			self.ids.shuffleimage.source=shuffleon
			print ("Shuffle On")
		self.num = 0
		self.dir = 0


	def next_file(self,direction):
		self.num += direction
		if self.shuffle == True:
			self.level = 'artist'
			try:
				self.next_Song = self.shufflelist[self.num]				#try opening the shufflelist and playing the specified song
			except:
				self.shufflelist = []									#if list doesnt exist:
				for x in table.distinct('location'):
					self.shufflelist.append(x['location'])				#add all songs to the list
					shuffle(self.shufflelist)							#shuffle the list
				self.next_Song = self.shufflelist[self.num]				#then try opening the specified song
		else:
			songlist = []
			tracklist = []
			for song in table.find(artist = tagger.artist, album = tagger.album):
				songlist.append(str(song['location']))
				tracklist.append(int(song['track']))
			tracksort = sorted(zip(tracklist,songlist))
			sortedtitle = [title for track, title in tracksort]
			try:
				print (songlist)
				self.dir += direction
				self.next_Song = sortedtitle[self.dir]
				print (self.dir)
			except:
				self.dir = 0
				self.next_Song = sortedtitle[self.dir]
				print (self.dir)
		self.media = self.instance.media_new_path(self.next_Song)
		self.player.set_media(self.media)
		self.player.play()
		self.refresh_Screen(self.next_Song)
		self.ids.playpausebutton.source = pauseicon
		print (self.next_Song)


	def next_button(self):
		self.next_file(1)

	def back_button(self):
		self.next_file(-1)

	def refresh_Screen(self,song):
		x = table.find_one(location=song)
		try:
			art = x['albumart']
		except:
			print ("art wasnt found")
		root, filename = os.path.split(song)
		tagger.filetagger(root, filename)
		self.songinfoupdate(song)
		self.slider_max(song)
		self.browser("refresh")
		self.cpu_counter()
		try:
			self.album_art.source=art
		except:
			self.album_art.source='data/icons/unknown.png'

	#called every time specified in the configuration
	def refresh(self, dt):
		self.perf_counter()
		state = str(self.player.get_state())
		duration = int(self.player.get_length()/1000)
		position = int(self.player.get_time()/1000)
		if position == -1:
			return
		#change time from seconds to minutes and seconds
		m, s = divmod(position, 60)
		if s < 10:
			s = '%02d' %s
		#update song position text
		try:
			self.ids.songpos.text = "{0}:{1}".format(m, s)
			remainder = duration - int(position)
			m, s = divmod(remainder, 60)
			if s < 10:
				s = '%02d' %s
			#update remaining time left on song and slider
			self.ids.songlength.text = "{0}:{1}".format(m, s)
			self.slider.value = position / screenupdatetime
			if state == "State.Ended":
				print ("{0} ended".format(self.title))
				self.level = 'artist'
				self.next_button()
		except:
			pass



	def play_title(self, search_artist, search_album, search_title):	#send artist album and title and this will play the file and refresh the screen
		self.artist = search_artist
		self.album = search_album
		self.title = search_title
		for title in table.find(artist = search_artist, album = search_album, title = search_title ):
			search_results = (str(title['location']))
			print (search_results)
			if os.path.isfile(search_results):
				self.media = self.instance.media_new_path(search_results)
				self.player.set_media(self.media)
				self.player.play()
				self.refresh_Screen(search_results)
				self.ids.playpausebutton.source = pauseicon
			else:
				pass


	def slider_max(self, song):
		for x in table.find(location=song):
			length = x['length']
		#returns the max for the song length slider (max value depends on how quickly it gets updated)
		self.slider.max = length / screenupdatetime
		print (self.slider.max)


	def volslider(self, value):
		self.player.audio_set_volume(int(value))

	def volstartup(self):
		volume = App.get_running_app().config.get('General','startupvolume')
		self.player.audio_set_volume(int(volume))
		return int(volume)


	#take song, look up file in database, extract artist album, and title
	def songinfoupdate(self, song):
		for x in table.find(location = song):
			artist = str(x['artist'])
			album = str(x['album'])
			title = str(x['title'])
			bitrate = str(x['bitrate'])
			size = str(x['size'])
			track = str(x['track'])
			#if the song is over 30 characters, limit it
			if len(artist) > 30:
				artist = (artist[:30] + '...')
		#update bigscreen info
		self.ids.songinformation.text = "{0}  --  {1}".format(artist,title)
		self.ids.bigscreenartist.text = artist
		self.ids.bigscreentitle.text = title
		self.ids.bigscreenalbum.text = album

	def perf_counter(self):
		try:
			self.ids.CPU.text = "CPU: " + str(psutil.cpu_percent()) + "%"
			self.ids.RAMpc.text = "RAM Used: " + str(psutil.virtual_memory().percent) + "%"
		except:
			pass
		#self.ids.RAM.text = ": " + str(round(psutil.virtual_memory().total/1024/1024/1024, 2)) + "GB"

	def perf_graph(self):
		global graph
		cpugraph = self.cpugraph
		cpuplot= MeshLinePlot(color=[1,0,1])
		ramgraph = self.ramgraph
		RAMplot= MeshLinePlot(color=[0,1,0])
		while True:
			for key in ['cpu','RAMpc']:
				if len(graph[key])>= 100:
					del graph[key][0]
					if len(graph[key])>= 100:
						del graph[key][0]
						#print (plot)
						#self.cpugraph.remove_plot(plot)
			graph['cpu'].append(int(psutil.cpu_percent()))
			graph['RAMpc'].append(psutil.virtual_memory().percent)
			RAMplot.points = [(i, j) for i, j in enumerate(graph['RAMpc'])]
			cpuplot.points = [(i, j) for i, j in enumerate(graph['cpu'])]
			try:
				self.ramgraph.add_plot(RAMplot)
				self.cpugraph.add_plot(cpuplot)
			except:
				pass
			#print (graph['cpu'])
			time.sleep(0.6)

	def start_thread(self,dt):
		global graph
		graph = defaultdict(list)
		graphdaemon = Thread(target = self.perf_graph)
		graphdaemon.daemon = True
		graphdaemon.start()
#_______________________________#MAIN APP#______________________________

class MainApp(App):

	def build(self):
		self.settings_cls = MySettings
		self.icon = 'music.png'
		build = Builder.load_file('carputer.ky')
		build.add_widget(PlayButtons())
		build.add_widget(VolumeSlider())
		build.add_widget(BigScreenInfo())
		#build.add_widget(Scroller1())
		#build.add_widget(Scroller2())
		return build

	def build_config(self,config):
		config.setdefaults("Default", {
			"resolutions": initialize.current_res(),
			"fullscreen": '1',
			"wallpaper": "blackbox.jpg",
			"startupvolume": 75,
			"bt_list": "Click to connect..."})
	def on_start(self):
		s = self.create_settings()
		self.root.ids.settingsscreen.add_widget(s)


	def build_settings(self,settings):
		#pull from settings.py
		data = settings.json_settings
		settings.add_json_panel("Default", self.config, data=data)


	def on_config_change(self,config,section,key,value):
		title = "Settings"
		if key == "startupvolume":
			self.startupvolume = int(value)
			message = "Volume changed to {}".format(value)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=2)
		if key == "bt_list":
			message = "Connected to {}".format(value)

		if key == "resolutions":
			x = value.split('x')
			height = int(x[1])
			width = int(x[0])
			Window.size = width,height
		if key == "fullscreen":
			print (value)
			if value == '1':
				Window.fullscreen = True
			else:
				Window.fullscreen = False
		if key == "wallpaper":
			wp = 'data/wallpapers/' + value
			wpfile = os.getcwd() + "\\data\\wallpapers\\{}".format(value)
			if os.path.isfile(wpfile):
				self.root.ids.wallpp.source = wp

			else:
				print (wp + " is not a valid background image")

if __name__ == "__main__":
	MainApp().run()
