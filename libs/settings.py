from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.settings import SettingsWithNoMenu, SettingOptions, SettingsWithSidebar, SettingItem
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.button import Button


class SettingSpacer(Widget):
    # Internal class, not documented.
    pass

class SettingSlider(SettingItem):
	popup = ObjectProperty(None, allownone=True)
	def on_panel(self, instance, value):
		if value is None:
			return
		self.bind(on_release=self._create_popup)

	def _set_option(self, instance):
		self.value = instance.text
		self.popup.dismiss()

	def _create_popup(self, instance):
		# create the popup
		self.options = "10"
		content = BoxLayout(orientation='vertical', spacing='5dp')
		popup_width = min(0.95 * Window.width, dp(500))
		self.popup = popup = Popup(
		    content=content, title=self.title, size_hint=(None, None),
		    size=(popup_width, '400dp'))
		popup.height = len(self.options) * dp(55) + dp(150)

		content.add_widget(Widget(size_hint_y=None, height=1))
		uid = str(self.uid)
		slider = Slider(min=0,max=100,orientation='horizontal')
		content.add_widget(slider)

		content.add_widget(SettingSpacer())
		btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
		btn.bind(on_release=popup.dismiss)
		slider = Slider(min=0,max=100,orientation='horizontal')
		content.add_widget(btn)
		popup.open()
