 #!/usr/bin/python


def loader():
	from importlib import util
	Modules = ['kivy','obd','mutagen','vlcpy','eyed3', 'dataset', 'pyusb']
	for module in Modules:
		print ("Looking for {}".format(module))
		find = util.find_spec(module)
		if find is None:
			raise Exception('Cant find module {0}, you can install using pip! (pip install {0})'.format(module))
		else:
			print ("FOUND: module {}".format(module))
loader()


#kivy imports
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock

#layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

#widgets
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

#misc

from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition

#garden imports
from kivy.garden.mapview import MapView

#non kivy imports
from time import time
from random import shuffle
from multiprocessing import Process
import re, sys, os, random, threading, time, eyed3, mutagen, glob, dataset, usb
from libs import tagger, audio, vlc



#==================CONFIGURATION========================================#
Window.fullscreen = False												#Fullscrean Boolean
Window.size = 1280,720 												    #Force a resolution, or just comment out
screenupdatetime = 0.5													#how fast slider and song info updates. use lower values for faster time, but more cpu work
startupvolume = 75														#change what volume the program starts at 0-100
MusicDirectory="/home/subcake/Music"									#change what folder PiCarputer looks in for your music
#=======================================================================#
Config.read('config.ini')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '450')
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


#-----------------------------#KIVY#------------------------------------
class ScreenManagement(ScreenManager):
    pass
class Menu(Screen):
	pass
class MusicScreen(Screen):
	pass
class MapScreen(Screen):
    pass
class CamScreen(Screen):
    pass
class BluetoothScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass
class OBDIIScreen(Screen):
	pass
class Root(Screen):
	pass
class VolumeSlider(BoxLayout):
	pass
class PlayButtons(AnchorLayout):
	pass
class Browser(BoxLayout):
	pass
class Scroller1(FloatLayout):
	pass
class Scroller2(FloatLayout):
	pass
class Show(FloatLayout):
	pass
class BigScreenInfo(BoxLayout):
	pass
class Zoom(BoxLayout):
	pass
class CenterGPS(BoxLayout):
	pass


#-----------------------MAIN-FUNCTIONS---------------------------------#				
class MainThread(AnchorLayout):
	# instance = vlc.libvlc_new(0,"C:/test.wav")
	# player = instance.media_player_new()
	# media = instance.media_new_path("unknown")
	# player.set_media(media)
	player = vlc.MediaPlayer("/path/to/file.flac")
	splash = int(1)
	
	
	def __init__(self, **kwargs):
		super(MainThread ,self).__init__(**kwargs)
		Clock.schedule_interval(self.songpos_callback, screenupdatetime)
		Clock.schedule_interval(self.mapupdate, screenupdatetime)
		self.buttonlist=[]
		self.artistlist=[]
		self.artistlistbool = False
		self.latitude = 41.257160
		self.longitude = -95.995102
		self.level = "artist"
		self.notshuffled = []
		self.num = 0
		self.shuffle = True
		self.dir_num = 13
		self.hidden = False
		self.car_follow = False
		self.artist_loaded = False
		self.artist = ''
		self.album = ''
		self.title = ''


	
	def gps_center(self):
		if self.car_follow == True:
			self.car_follow = False
		else:
			self.car_follow = True
		print (self.car_follow)	
		
	def mapupdate(self,dt):
		if self.car_follow:
			self.ids.mapview.center_on(self.latitude,self.longitude)
		else:
			pass
			
	def gps_start(self):
		t = threading.Thread(target = self.gps_initiate)
		t.start()
		
	def gps_initiate(self):	
		import gps
		try:
			self.ids.mapmarker.lat = gps.Latitude
			self.ids.mapmarker.lon = gps.Longitude
			self.ids.latitude.text = str(gps.Latitude)
			self.ids.longitude.text = str(gps.Longitude)
			self.ids.speed.text = str(gps.Speed)
			self.ids.satellites.text = str(gps.Satellites)
		except:
			pass


		
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
		try:
			self.album_art.source=art
		except:
			self.album_art.source='data/icons/unknown.png'
				
			


	def songpos_callback(self, dt):										#called every time specified in the configuration
		state = str(self.player.get_state())
		duration = int(self.player.get_length()/1000)
		position = int(self.player.get_time()/1000)
		if position == -1:
			return
		m, s = divmod(position, 60) 									#change time from seconds to minutes and seconds
		if s < 10:
			s = '%02d' %s
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
	
	
	def browser(self,instance):		
		if instance == "back":
			if self.level == "artist":
				self.scrollviewbrowser()
			elif self.level == "album":
				self.level = "artist"
				self.scrollviewbrowser()
			elif self.level == "title":
				self.level = "album"
				self.scrollviewbrowser()
				
		elif instance == "refresh":
			self.scrollviewbrowser()

		else:
			if self.level == "artist":
				self.level = "album"
				self.artist = instance.text
				self.scrollviewbrowser()
			elif self.level == "album":
				self.level = "title"
				self.album = instance.text
				self.scrollviewbrowser()
			elif self.level == "title":
				self.title = instance.text
				self.play_title(self.artist,self.album,self.title)


		
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
		
		
	def songinfoupdate(self, song):										#take song, look up file in database, extract artist album, and title
		for x in table.find(location = song):							
			artist = str(x['artist'])
			album = str(x['album'])
			title = str(x['title'])
			bitrate = str(x['bitrate'])
			size = str(x['size'])
			track = str(x['track'])
			if len(artist) > 30:
				artist = (artist[:30] + '...') 
		self.ids.songinformation.text = "{0}  --  {1}".format(artist,title)
		self.ids.bigscreenartist.text = artist
		self.ids.bigscreentitle.text = title
		self.ids.bigscreenalbum.text = album
		
	def movebrowser(self):
		if self.hidden == True:
			self.album_art.pos_hint = {'y':0.,"x":0.2}
			self.ids.hiddeninfo.pos_hint = {'y':-2,"x":0}
			self.browsermove.x = 0
			if self.level =='artist':
				self.ids.artistscroller.pos_hint = {'x':0}
			else:
				self.ids.albumscroller.pos_hint = {'x':0}
			self.ids.showbrowser.x = -100
			self.hidden = False
		else:
			self.album_art.pos_hint = {'y':0,"x":-.2}
			self.ids.hiddeninfo.pos_hint = {"x": 0.49, 'y': 0.1}
			self.browsermove.x = -5000
			self.ids.artistscroller.pos_hint = {'x': -2, 'y':0}
			self.ids.albumscroller.pos_hint = {'x': -2, 'y':0}
			self.ids.showbrowser.x = 0
			self.hidden = True

	def refresh_scrollviewbrowser(self):
		for x in self.artistlist:
			self.ids.scroller1.remove_widget(x)
		self.artistlistbool=False
		self.scrollviewbrowser()


	def scrollviewbrowser(self,*args):
		lastalbum = ''
		if self.level=='artist':
			if self.hidden == True:
				pass
			else:
				if self.artistlistbool == True:
					self.ids.artistscroller.pos_hint = {"x": 0}
					self.ids.albumscroller.pos_hint = {"x": -2}
				else:
					self.ids.artistscroller.pos_hint = {"x": 0}
					self.ids.albumscroller.pos_hint = {"x": -2}
					for x in table.distinct('artist'):
						btn = Button(id=unicode(x['artist']),text=unicode(x['artist']), size_hint_y=None, font_size=17, height=50)
						btn.bind(on_press=self.browser)
						self.artistlist.append(btn)
						self.ids.scroller1.add_widget(btn)
					self.artistlistbool = True

		elif self.level=='album':
			for x in self.buttonlist:
				self.ids.scroller2.remove_widget(x)
			self.ids.artistscroller.pos_hint = {"x": -2}
			self.ids.albumscroller.pos_hint = {"x": 0}
			for x in table.find(artist=self.artist):
				if x['album'] == lastalbum:
					pass
				else:
					btn = Button(text=unicode(x['album']),size_hint_y=None, font_size=17, height=50)
					btn.bind(on_press=self.browser)
					self.buttonlist.append(btn)
					self.ids.scroller2.add_widget(btn)
					lastalbum = x['album']
					
		elif self.level=='title':
			for x in self.buttonlist:
				self.ids.scroller2.remove_widget(x)
			self.ids.artistscroller.pos_hint = {"x": -2}
			self.ids.albumscroller.pos_hint = {"x": 0}
			for x in table.find(artist=self.artist,album=self.album):
				btn = Button(text=unicode(x['title']), size_hint_y=None, font_size=17, height=50)
				btn.bind(on_press=self.browser)
				self.buttonlist.append(btn)
				self.ids.scroller2.add_widget(btn)

	def camsetup(self):
		from kivy.uix.camera import Camera
		for x in range(0,2):
			try:
				self.ids['camera'].index = x
			except:
				print ("failed {0}".format(x))
				
	def startusb(self):
		audio.connect('22b8','2ea4')

	def filesearcher():
		for root, directories, filenames in os.walk(str(MusicDirectory)):
			for filename in filenames:
				ext = [".mp3",".m4a",".flac"]
				for x in ext:
					if filename.endswith(x):
						location = os.path.join(root,filename)
						if table.find_one(location=location):
							pass
						else:
							print ("passing to filetagger", filename)
							tagger.filetagger(root,filename)							
	filesearcher()

	splash=0

#_______________________________#MAIN APP#______________________________

class MainApp(App):
	
	
	def build(self):
		self.icon = 'music.png'
		sc1 = Scroller1()
		sc2 = Scroller2()
		gps = CenterGPS()
		zoom = Zoom()
		bigscreeninfo = BigScreenInfo()
		show = Show()
		browser = Browser()
		volumeslider = VolumeSlider()
		playbuttons = PlayButtons()
		build = Builder.load_file('carputer.ky')
		build.add_widget(playbuttons)
		build.add_widget(volumeslider)
		build.add_widget(browser)
		build.add_widget(show)
		build.add_widget(bigscreeninfo)
		build.add_widget(zoom)
		build.add_widget(gps)
		build.add_widget(sc1)
		build.add_widget(sc2)
		return build




if __name__ == "__main__":
	MainApp().run()


