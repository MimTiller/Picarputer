 #!/usr/bin/python

#kivy imports
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.config import Config, ConfigParser
from kivy.clock import Clock
from kivy_garden.graph import MeshLinePlot, SmoothLinePlot
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
from kivy.uix.camera import Camera
#kivyMD imports

from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import *
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import *
from kivymd.uix.label import *
from kivymd.uix.behaviors import (
    CircularElevationBehavior,
    CircularRippleBehavior,
    CommonElevationBehavior,
    RectangularElevationBehavior,
    RectangularRippleBehavior,
    SpecificBackgroundColorBehavior,)
from kivymd.theming import ThemableBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.theming import ThemeManager
from kivymd.uix.dropdownitem import MDDropDownItem

#misc
from kivy.properties import (
    BooleanProperty,
    BoundedNumericProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,)

from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition
from kivy.utils import get_color_from_hex as rgb
from kivy.graphics import *
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.event import EventDispatcher
#non kivy imports
from time import time
from random import shuffle
from multiprocessing import Process
import re, sys, os, random, threading, time, eyed3, mutagen, glob
import dataset, usb, psutil, importlib, json, concurrent.futures
from libs import tagger, audio, vlc, btdevices, initialize, settings, speech,source_control
from libs.settings import SettingSlider, MySettings
#from libs.spotify import spotify_control as spotify
from threading import Thread
from collections import defaultdict
from os import path
from functools import partial

import asyncio
import speech_recognition as sr
#==================CONFIGURATION========================================#
									    								#Force a resolution, or just comment out
screenupdatetime = 0.5
musicupdatetime = 1													#how fast slider and song info updates. use lower values for faster time, but more cpu work
MusicDirectory='/home/subcake/Music'									#change what folder PiCarputer looks in for your music
#=======================================================================#



db = dataset.connect('sqlite:///songlist.db')
table = db['songs']
settingsdb = db['settings']
global graph





#--------------------------------#KIVY#------------------------------------
#pass clickable button behavior
class IconButton(ButtonBehavior,BoxLayout):
	pass
class ScreenManagement(ScreenManager):
    pass
class Menu(AnchorLayout):
	pass
class MusicScreen(MDScreen,EventDispatcher):
	pass
class SettingsScreen(MDScreen):
	pass
class OBDIIScreen(MDScreen):
	pass
class PerfScreen(MDScreen):
	pass
class Root(MDScreen):
	pass
class VolumeSlider(AnchorLayout):
	pass
class Source(MDDropDownItem):
	pass
class Notify(FloatLayout):
	pass
class DynamicLabel(MDLabel):
	multiplier = NumericProperty(1)

class IconSizer(MDIconButton):
	multiplier = NumericProperty(1)

class VoiceRecognizer(MDIconButton):
	pass

class WallPaper(Image):
	wallpaper_selection = StringProperty()
	config = ConfigParser()
	config.read('carputer.ini')
	try:
		wallpaper = config.get('Default', 'wallpaper')
	except:
		wallpaper = 'blackbox.jpg'
	wpd = str('data/wallpapers/' + wallpaper)
	wallpaper_selection = wpd




#-----------------------MAIN-FUNCTIONS---------------------------------#
class MainThread(FloatLayout):
	title = StringProperty('')
	artist = StringProperty('')
	album = StringProperty('')
	albumart = StringProperty('')

	def __init__(self, **kwargs):
		super(MainThread ,self).__init__(**kwargs)
		self.threads = [self.perf_graph]
		Clock.schedule_once(partial(self.start_threads,targets=self.threads),1)
		Clock.schedule_interval(self.refresh, screenupdatetime)
		Clock.schedule_once(self.start_song_update,3)
		Window.bind(on_resize=self.on_window_resize)
		self.font_scaling = NumericProperty()
		self.wallpaperlist = ListProperty()

		self.is_playing = False
		self.shuffle_state = False
		self.source_pass = False
		self.currentscreen = 1
		self.source = App.get_running_app().config.get('Default','audio_source')

	def start_song_update(self,dt):
		Clock.schedule_interval(self.songinfoupdate, musicupdatetime)
	#cosmetic functions

	#kivy callback, called everytime the window size changes
	def on_window_resize(self,window,width,height):
		self.icon_font_update()

	def icon_font_update(self):
		for icon in ['shuffle','previous_track','playpause','next_track']:
			multiplier = self.ids[icon].multiplier
			self.ids[icon].user_font_size = self.icon_size(multiplier)

		for button in ['musicicon','obdicon','perficon','settingsicon']:
			icon = button[:-4]
			self.ids[icon].user_font_size = self.ids[button].size[1]/1.1

	def icon_size(self,multiplier):
		width = Window.width
		size = width * .1 * multiplier
		size = str(size) + 'sp'
		return(size)

	def font_update(self):
		width = Window.width
		for text in ['bigscreenartist','bigscreentitle','bigscreenalbum','source_label']:
			multiplier = self.ids[text].multiplier
			text_length = len(self.ids[text].text)
			if text_length > 50:
				scale = 1.5
				multiplier = multiplier/scale
			size = width * 0.05 * multiplier
			self.ids[text].font_size = size

	def show_voice(self):
		print('starting voice animation..')
		voice_button = self.ids.voicecontrol
		anim = Animation(pos_hint={'y':0.5},duration=0.5)
		anim.start(voice_button)
		Clock.schedule_once(self.hide_voice,1)

	def hide_voice(self,dt):
		voice_button = self.ids.voicecontrol
		anim = Animation(pos_hint={'y':0.9},duration=0.5)
		anim.start(voice_button)

	def notify(self,widget,title,message,timeout):
		print('(main.py) notify:')
		notification = widget.root.ids.notify
		msg = widget.root.ids.notifymessage
		msg.text = str(message)
		ttl = widget.root.ids.notifytitle
		ttl.text = str(title)
		anim = Animation(pos_hint={'x':0.72},duration=.3)
		anim.start(notification)
		Clock.schedule_once(partial(self.hide_notify,self,widget),float(timeout))

	def hide_notify(self,widget,*args):
		notification = widget.root.ids.notify
		anim = Animation(pos_hint={'x':1},duration=.3)
		anim.start(notification)

	def slide_screen(self,instance,screenname):
		for button in ['music','obd','perf','settings']:
			self.ids[button].text_color = CarputerApp().theme_cls.primary_color
			self.ids[str(button + 'label')].color = CarputerApp().theme_cls.primary_color
		self.ids[screenname].text_color = CarputerApp().theme_cls.accent_color
		self.ids[str(screenname + 'label')].color = CarputerApp().theme_cls.accent_color
		if int(instance) > int(self.currentscreen):
			self.ids.st.transition = SlideTransition(direction='left')
			self.currentscreen = instance
		elif int(instance) < int(self.currentscreen):
			self.ids.st.transition = SlideTransition(direction='right')
			self.currentscreen = instance
		else:
			pass
		self.ids.st.current = screenname


	#sets the current audio source
	def set_source(self,button):
		source_names = {'spotify':'Spotify','usb':'USB','video-input-component':'Aux','bluetooth':'Bluetooth'}
		self.source = source_names[button.icon]
		self.ids.source_button.icon = button.icon
		self.ids.source_label.text = source_names[button.icon]
		self.remove_widget(button.parent)
		self.source_pass = False

	#called when the source button is clicked
	def select_source(self,source):
		if self.source_pass == True:
			pass
		else:
			source_icons = ['spotify','usb','video-input-component','bluetooth']
			b = BoxLayout(orientation='vertical',size_hint=(0.01,0.04),x=source.x,y=source.y-(source.height*len(source_icons)))

			for icon in source_icons:
				m = MDIconButton(icon=icon,theme_text_color='Custom',text_color=CarputerApp().theme_cls.primary_color)
				m.bind(on_release=self.set_source)
				b.add_widget(m)
			with b.canvas:
				Color(.9,.9,.9,.1)
				b.rect = RoundedRectangle(pos=b.pos,size=(b.x/24,b.y/2),radius=(20,20,20,20))
			self.add_widget(b)
			self.source_pass = True

	#playback control functions:
	def control(self,control_msg):
		#get current source:
		source_control.control_playback(control_msg,self.source)


	#refreshers
	def refresh(self, dt):
		self.perf_counter()
		self.font_update()
		if self.is_playing == True:
			self.ids.playpause.icon = 'pause'
		else:
			self.ids.playpause.icon = 'play'

		if self.shuffle_state == True:
			self.ids.shuffle.text_color = CarputerApp().theme_cls.accent_color
		else:
			self.ids.shuffle.text_color = CarputerApp().theme_cls.primary_color

		#if is_shuffle:
			#self.ids.shuffle.text_color = CarputerApp().theme_cls.accent_color
		#else:
			#self.ids.shuffle.text_color = CarputerApp().theme_cls.primary_color



	#initialization (called on startup)
	def set_volume(self, value):
		self.source = source
		source_control.control_playback(value,self.source)

	def volstartup(self):
		try:
			volume = App.get_running_app().config.get('Default','startupvolume')
		except:
			print('volstartup: couldnt get volume from config')
			volume = 75
		#self.player.audio_set_volume(float(volume))
		return int(float(volume))


	oldtrack = ''
	#display all the song info on the music screen
	def songinfoupdate(self,dt):
		#send source to source_control.py and return a dict to pull track info from
		track = source_control.get_track_info(self.source)
		if track == None:
			pass
		else:
			try:
				self.albumart = source_control.get_album_art(self.source,track)
				self.is_playing = track['is_playing']
				self.shuffle_state = track['shuffle_state']
				if not track['position']:
					print('Not playing currently')
				pos = int(track['position']/1000)
				dur = int(track['duration']/1000)
				if track['track'] == self.oldtrack:
					pass
				else:
					print('(main.py) new track')
					artist = track['artist']
					album = track['album']
					title = track['track']
					art = track['art']
					print('(main.py) {} : {} : {}'.format(artist,album,title))
					#update bigscreen info
					self.artist = artist
					self.title = title
					self.album = album
					self.ids.album_art.reload()
					self.oldtrack = track['track']
				#change time from seconds to minutes and seconds
				m, s = divmod(pos, 60)
				if s < 10:
					s = '%02d' %s
				#update song position text
				try:
					self.ids.songpos.text = '{0}:{1}'.format(m, s)
					m, s = divmod(dur, 60)
					if s < 10:
						s = '%02d' %s
					#update remaining time left on song and slider
					self.ids.songlength.text = '{0}:{1}'.format(m, s)
					self.slider.max = dur
					self.slider.value = pos
				except Exception as e:
					print('(songinfoupdate) failed to update time')
					print(e)
			except Exception as e:
				print(e)



	def perf_counter(self):
		try:
			self.ids.CPU.text = 'CPU: ' + str(psutil.cpu_percent()) + '%'
			self.ids.RAMpc.text = 'RAM Used: ' + str(psutil.virtual_memory().percent) + '%'

		except:
			pass

		#self.ids.RAM.text = ': ' + str(round(psutil.virtual_memory().total/1024/1024/1024, 2)) + 'GB'

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
			except Exception as e:
				print('(perf_graph) {}'.format(e))
			time.sleep(screenupdatetime)

	def start_threads(self,dt,targets):
		global graph
		graph = defaultdict(list)
		print('(main.py) starting threads: {}'.format([x.__name__ for x in targets]))
		for target in targets:
			daemon = Thread(target = target)
			daemon.daemon = True
			daemon.start()

#_______________________________#MAIN APP#______________________________

class CarputerApp(MDApp):
	def __init(self,**kwargs):
		self.theme_cls.theme_style = 'Dark'
		#load the config file
		self.config = ConfigParser()
		self.config.read('carputer.ini')
		self.timeout = NumericProperty()



	def build(self):
		#declare the settings class
		self.settings_cls = MySettings
		#set an icon
		self.icon = 'music.png'
		#set primary and accent colors from config
		self.theme_cls.primary_palette = self.config.get('Default', 'themecolor')
		self.theme_cls.accent_palette	= self.config.get('Default', 'accentcolor')
		print('(main.py) Initializing: Theme Color ({}) and Accent Color ({}) set'.format(self.theme_cls.primary_palette,self.theme_cls.accent_palette))


	def build_config(self,config):
		self.config.setdefaults('Default', {
			'resolutions': initialize.current_res(),
			'fullscreen': 0,
			'wallpaper': 'blackbox.jpg',
			'startupvolume': 75,
			'audio_source': 'Spotify',
			'bt_list': 'Click to connect...',
			'notificationtimeout':2,
			'themecolor': 'Blue',
			'accentcolor': 'Orange',
			'audio_output':'None'})



	def on_start(self):
		s = self.create_settings()
		self.root.ids.settingsscreen.add_widget(s)
		print('(main.py) Initializing: Settings Created')

		try:
			#Get config resolution
			conf_res = self.config.get('Default', 'resolutions').split('x')
			confh = int(conf_res[1])
			confw = int(conf_res[0])
			#Set Resolution
			Window.size = confw,confh
			#check Fullscreen
			fs = self.config.get('Default', 'fullscreen')
			self.timeout = self.config.get('Default','notificationtimeout')
			if fs == '1':
				Window.fullscreen = True
			elif fs == '0':
				Window.fullscreen = False
			Window.top=30
			Window.left=0

			Window.size = confw,confh
			print('(main.py) Initializing: resolution ({}x{}) and fullscreen mode ({}) set'.format(confw,confh,fs))

		except Exception as e:
			print('error: {}'.format(e))
			self.timeout = 1
			#get current screen resolution
			x = initialize.current_res().split('x')
			height = int(x[1])
			width = int(x[0])
			Window.size = width,height
			Window.fullscreen=False
		print('(main.py) Initializing: finished startup ')

	def build_settings(self,settings):
		with settings.canvas.before:
			settings.canvas.before.clear()
		with settings.canvas.before:
			Color(.1,.1,.1,0.65,mode='rgba')
			Rectangle(pos=(0,0), size=(10000,10000))
		data = settings.json_settings
		settings.add_json_panel('Default', self.config, data=data)
		print('(main.py) building settings...')

	def on_config_change(self,config,section,key,value):
		title = 'Settings'
		self.timeout = config.get('Default','notificationtimeout')

		if key == 'startupvolume':
			self.startupvolume = int(float(value))
			message = 'Volume changed to {}'.format(value)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)

		if key == 'bt_list':
			message = 'Connected to {}'.format(value)

		if key == 'resolutions':
			x = value.split('x')
			height = int(x[1])
			width = int(x[0])
			Window.size = width,height
			message = 'Resolution set to {}'.format(value)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)

		if key == 'fullscreen':
			print (value)
			if value == '1':
				Window.fullscreen = True
				fullscreen= 'turned on'
			else:
				Window.fullscreen = False
				fullscreen = 'turned off'
			message = 'fullscreen {}'.format(fullscreen)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)

		if key == 'wallpaper':
			wp = 'data/wallpapers/' + value
			wpfile = os.getcwd() + '\\data\\wallpapers\\{}'.format(value)
			if os.path.isfile(wpfile):
				self.root.ids.wallpp.source = wp
			else:
				print (wp + ' is not a valid background image')

		if key == 'notificationtimeout':
			title = 'Notify'
			message = 'Changed Notify timeout to {} Seconds'.format(value)
			self.timeout = value
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)

		if key == 'themecolor':
			message = 'Changed main theme color to {}'.format(value)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)
			self.theme_cls.primary_palette = value

		if key == 'accentcolor':
			message = 'Changed accent color to {}'.format(value)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)
			self.theme_cls.accent_palette = value

		if key == 'default_source':
			message = 'Changed audio source to {}'.format(value)
			MainThread.notify(MainThread,self,title=title,message=message,timeout=self.timeout)
			MainThread.set_source(value)

if __name__ == '__main__':
	CarputerApp().run()
