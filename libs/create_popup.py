from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp


def _input_popup(self,text):
	content=BoxLayout()
	txt_input=TextInput(text=text)
	btnbox=BoxLayout(orientation='horizontal')
	btn = Button(text = "OK")
	content.add_widget(txt_input)
	btnbox.add_widget(btn)
	content.add_widget(btnbox)
	popup_width = min(0.95 * Window.width, dp(300))
	popup_height = min(0.95 * Window.height, dp(400))
	self.popup = Popup(
	content=content, title='', size_hint=(None, None),
	size=(popup_width, popup_height))
	self.popup.open()
