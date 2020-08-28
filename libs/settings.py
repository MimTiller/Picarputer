from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.settings import SettingsWithNoMenu, SettingOptions, SettingItem, SettingsWithSidebar
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.compat import string_types, text_type
from kivy.graphics import Color
from kivy.animation import Animation
from kivy.config import Config, ConfigParser
import importlib, os, json



class SettingSpacer(Widget):
    # Internal class, not documented.
    pass



class SettingSlider(SettingItem):
	from kivy.lang import Builder
	value = ObjectProperty('int')
	popup = ObjectProperty(None, allownone=True)
	slidermax = NumericProperty()
	def on_panel(self, instance, value):
		if value is None:
			return
		self.bind(on_release=self._create_popup)

	def _set_option(self,option):
		print (option)
		self.value = int(option)
		self.popup.dismiss()

	def _create_popup(self, instance):
		# create the popup
		print (self.value)
		label = Label(text=str(int(self.value)),id='labelvalue')
		def on_value(self,value):
			label.text=str(int(value))
			self.value = int(value)

		self.options = "10"
		content = BoxLayout(orientation='vertical', spacing='5dp')
		popup_width = min(0.95 * Window.width, dp(500))

		btn2 = Button(text='Ok',size_hint_y=None, height=dp(50))
		btn2.bind(on_release=lambda x:self._set_option(int(float(label.text))))
		self.popup = popup = Popup(
		    content=content, title=self.title, size_hint=(None, None),
		    size=(popup_width, '400dp'))
		popup.height = len(self.options) * dp(55) + dp(150)

		content.add_widget(Widget(size_hint_y=None, height=1))
		uid = str(self.uid)
		slider = Slider(min=0,max=int(float(self.slidermax)),orientation='horizontal',step=1,value=self.value)
		slider.bind(value = on_value)

		content.add_widget(slider)
		content.add_widget(label)

		content.add_widget(SettingSpacer())
		btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
		btn.bind(on_release=popup.dismiss)
		content.add_widget(btn)
		content.add_widget(btn2)
		popup.open()

class SettingScrollview(SettingItem):
	function_string = StringProperty()
	popup = ObjectProperty(None, allownone=True)
	value = StringProperty()


	def on_panel(self, instance, value):
		if value is None:
			return
		self.bind(on_release=self._create_popup)

	def _set_option(self,button):
		print ("option set to ", button.text)
		self.value = button.text
		self.popup.dismiss()


	def _create_popup(self, instance):
		mod_name, func_name= self.function_string.rsplit('.',1)
		mod = importlib.import_module(mod_name)
		func = getattr(mod,func_name)
		self.options = func()
		# create the popup
		content = BoxLayout(orientation='vertical')
		grid = GridLayout(cols=1,spacing='2dp',size_hint_y=None)
		scroll = ScrollView()

		for option in self.options:
			btn = Button(text=option, size_hint_y=None,height=40)
			btn.bind(on_press=self._set_option)
			print(btn.text)
			grid.add_widget(btn)

		okbutton = Button(text="Cancel",size_hint_y=0.1)

		grid.height = len(self.options) * 40
		scroll.add_widget(grid)
		content.add_widget(scroll)
		content.add_widget(okbutton)

		popup_width = min(0.95 * Window.width, dp(500))
		self.popup = popup = Popup(
			content=content, title=self.title, size_hint=(None, None),
			size=(popup_width, '400dp'))
		okbutton.bind(on_press=self.popup.dismiss)
		popup.height = Window.height
		grid.bind(minimum_height=content.setter('height'))
		popup.open()

class MySettings(SettingsWithNoMenu):
	json_settings = json.dumps([
		{'type': 'scrollview',
		'title': "Screen Resolution",
		'desc': "Set the screen resolution",
		'section':'Default',
		'key': 'resolutions',
		'function_string': 'libs.initialize.supported_res'},
		{'type': 'bool',
		'title': 'Fullscreen',
		'desc': 'Set window to be Fullscreen or Windowed',
		'section': 'Default',
		'key':'fullscreen'},
		{'type':'scrollview',
		'title': 'Wallpaper',
		'desc': 'Set your Wallpaper. You can add your own wallpapers to /data/wallpapers',
		'section':'Default',
		'key':'wallpaper',
		'function_string': 'libs.initialize.get_wallpapers'},
		{'type': 'title',
		'title': 'Sound'},
		{'type': 'slider',
		'title': 'Startup Volume',
		'desc': 'Set the default startup volume for the picarputer',
		'key': 'startupvolume',
		'section': 'Default',
		'slidermax':'100'},
		{'type': 'scrollview',
		'title': 'Bluetooth Devices',
		'desc': 'List and connect to compatible Bluetooth devices',
		'section': 'Default',
		'key': 'bt_list',
		'function_string': 'libs.btdevices.get_bluetooth_devices'},
		{'type': 'title',
		'title': 'Notifications'},
		{'type': 'slider',
		'title': 'Notification Timeout',
		'desc': 'Amount of time it takes for notification to dissapear',
		'section': 'Default',
		'key': 'notificationtimeout',
		'slidermax':'10'}
		])

	def __init__(self,*args,**kargs):
		super(MySettings,self).__init__(*args,**kargs)
		#color=(0,0,0,0)
		self.register_type('scrollview',SettingScrollview)
		self.register_type('slider',SettingSlider)
