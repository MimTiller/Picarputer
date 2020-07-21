 #!/usr/bin/python
#kivy imports

from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot, SmoothLinePlot
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
import re, sys, os, random, threading, time, eyed3, mutagen, glob, dataset, usb, psutil
from libs import tagger, audio, vlc, btdevices
from threading import Thread
from collections import defaultdict
from os import path
import concurrent.futures
#==================CONFIGURATION========================================#
Window.fullscreen = False												#Fullscrean Boolean
Window.size = 800,480 												    #Force a resolution, or just comment out
screenupdatetime = 0.5													#how fast slider and song info updates. use lower values for faster time, but more cpu work
startupvolume = 75														#change what volume the program starts at 0-100
MusicDirectory="/home/subcake/Music"									#change what folder PiCarputer looks in for your music
#=======================================================================#
#Window.fullscreen = True
Config.read('config.ini')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'borderless', 'True')
Config.set('graphics','resizable',0)
Config.write()





ProgDir="/home/subcake/Desktop/Picarputer"
ArtDir = "artwork"
update_length_milliseconds = screenupdatetime*1000
playicon = 'data/icons/play.png'
pauseicon = 'data/icons/pause.png'
db = dataset.connect('sqlite:///songlist.db')
table = db['songs']
global graph
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

#-----------------------MAIN-FUNCTIONS---------------------------------#
class MainThread(AnchorLayout):
	instance = vlc.Instance()
	player = instance.media_player_new("C:/test.wav")
	media = instance.media_new_path("unknown")
	player.set_media(media)
	player = vlc.MediaPlayer("/path/to/file.flac")
	splash = int(1)


	def __init__(self, **kwargs):
		super(MainThread ,self).__init__(**kwargs)
		Clock.schedule_interval(self.refresh, screenupdatetime)
		Clock.schedule_once(self.start_thread,0)

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
		self.wallpaper = 'data/wallpapers/blackbox.jpg'
		#self.splash = 1
		self.wallpaperlist = ListProperty()
		self.result = ListProperty
		self.currentscreen = 1

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

	def get_bluetooth_devices(self):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(btdevices.bluetooth_search)
			self.result = future.result()
			if self.result == []:
				print ("No Devices Found")
				self.result == ["None"]
			print (self.result)
			return self.result

	def get_wallpapers(self):
		cwd = os.getcwd() + "\\data\\wallpapers"
		self.wallpaperlist = [f for f in os.listdir(cwd)]
		#self.ids.wpspinner.text = files[0]
		#print (files[0])
		#self.ids.wpspinner.bind(text = self.on_spinner_select)
		return self.wallpaperlist


	def on_spinner_select(self,spinner,text):
		#text = self.ids.wpspinner.text
		self.ids.btspinner.text_autoupdate = BooleanProperty(True)
		if text == "bluetooth":
			print ("Yay you got the spinner to work")
		else:
			wp = 'data/wallpapers/' + text
			self.ids.wpspinner.text_autoupdate = BooleanProperty(True)
			wpfile = os.getcwd() + "\\data\\wallpapers\\{}".format(text)
			print (wpfile)
			if os.path.isfile(wpfile):
				with self.canvas.before:
					Rectangle(size=self.size,pos=self.pos,source=wp)
			else:
				print (wp + " is not a valid background image")


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

	def refresh(self, dt):										#called every time specified in the configuration
		state = str(self.player.get_state())
		duration = int(self.player.get_length()/1000)
		position = int(self.player.get_time()/1000)
		if position == -1:
			return
		m, s = divmod(position, 60) 									#change time from seconds to minutes and seconds
		if s < 10:
			s = '%02d' %s
		try:
			self.ids.songpos.text = "{0}:{1}".format(m, s) 					#update song position text
			remainder = duration - int(position)
			m, s = divmod(remainder, 60)
			if s < 10:
				s = '%02d' %s
			self.ids.songlength.text = "{0}:{1}".format(m, s)				#update remaining time left on song
			self.slider.value = position / screenupdatetime					#update slider
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
		self.player.audio_set_volume(int(startupvolume))
		return int(self.player.audio_get_volume())

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
		self.ids.CPU.text = "CPU: " + str(psutil.cpu_percent()) + "%"
		self.ids.RAMpc.text = "RAM Used: " + str(psutil.virtual_memory().percent) + "%"
		self.ids.RAM.text = ": " + str(round(psutil.virtual_memory().total/1024/1024/1024, 2)) + "GB"



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
			self.ramgraph.add_plot(RAMplot)
			self.cpugraph.add_plot(cpuplot)

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
		self.icon = 'music.png'
		sc1 = Scroller1()
		sc2 = Scroller2()
		bigscreeninfo = BigScreenInfo()
		volumeslider = VolumeSlider()
		playbuttons = PlayButtons()
		build = Builder.load_file('carputer.ky')
		build.add_widget(playbuttons)
		build.add_widget(volumeslider)
		build.add_widget(bigscreeninfo)
		build.add_widget(sc1)
		build.add_widget(sc2)
		return build




if __name__ == "__main__":
	MainApp().run()
