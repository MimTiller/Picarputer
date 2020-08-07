from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.settings import SettingsWithNoMenu, SettingOptions, SettingsWithSidebar
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.compat import string_types, text_type
from kivy.graphics import Color
import importlib, os


class SettingSpacer(Widget):
    # Internal class, not documented.
    pass

class SettingItem(FloatLayout):

    '''Base class for individual settings (within a panel). This class cannot
    be used directly; it is used for implementing the other setting classes.
    It builds a row with a title/description (left) and a setting control
    (right).
    Look at :class:`SettingBoolean`, :class:`SettingNumeric` and
    :class:`SettingOptions` for usage examples.
    :Events:
        `on_release`
            Fired when the item is touched and then released.
    '''

    title = StringProperty('<No title set>')
    '''Title of the setting, defaults to '<No title set>'.
    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to
    '<No title set>'.
    '''

    desc = StringProperty(None, allownone=True)
    '''Description of the setting, rendered on the line below the title.
    :attr:`desc` is a :class:`~kivy.properties.StringProperty` and defaults to
    None.
    '''

    disabled = BooleanProperty(False)
    '''Indicate if this setting is disabled. If True, all touches on the
    setting item will be discarded.
    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    section = StringProperty(None)
    '''Section of the token inside the :class:`~kivy.config.ConfigParser`
    instance.
    :attr:`section` is a :class:`~kivy.properties.StringProperty` and defaults
    to None.
    '''

    key = StringProperty(None)
    '''Key of the token inside the :attr:`section` in the
    :class:`~kivy.config.ConfigParser` instance.
    :attr:`key` is a :class:`~kivy.properties.StringProperty` and defaults to
    None.
    '''

    value = ObjectProperty(None)
    '''Value of the token according to the :class:`~kivy.config.ConfigParser`
    instance. Any change to this value will trigger a
    :meth:`Settings.on_config_change` event.
    :attr:`value` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    panel = ObjectProperty(None)
    '''(internal) Reference to the SettingsPanel for this setting. You don't
    need to use it.
    :attr:`panel` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    content = ObjectProperty(None)
    '''(internal) Reference to the widget that contains the real setting.
    As soon as the content object is set, any further call to add_widget will
    call the content.add_widget. This is automatically set.
    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    selected_alpha = NumericProperty(0)
    '''(internal) Float value from 0 to 1, used to animate the background when
    the user touches the item.
    :attr:`selected_alpha` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    '''

    __events__ = ('on_release', )
    def __init__(self, **kwargs):
        super(SettingItem, self).__init__(**kwargs)
        self.value = self.panel.get_value(self.section, self.key)


    def add_widget(self, *largs):
        if self.content is None:
            return super(SettingItem, self).add_widget(*largs)
        return self.content.add_widget(*largs)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return
        touch.grab(self)
        self.selected_alpha = 1
        return super(SettingItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.dispatch('on_release')
            Animation(selected_alpha=0, d=.25, t='out_quad').start(self)
            return True
        return super(SettingItem, self).on_touch_up(touch)

    def on_release(self):
        pass

    def on_value(self, instance, value):
        if not self.section or not self.key:
            return
        # get current value in config
        panel = self.panel
        if not isinstance(value, string_types):
            value = str(value)
        panel.set_value(self.section, self.key, value)

class SettingDynamicOptions(SettingOptions):
	function_string = StringProperty()
	def _create_popup(self,instance):
		mod_name, func_name= self.function_string.rsplit('.',1)
		mod = importlib.import_module(mod_name)
		func = getattr(mod,func_name)
		self.options = func()

		super(SettingDynamicOptions, self)._create_popup(instance)

class SettingSlider(SettingItem):
	popup = ObjectProperty(None, allownone=True)


	def on_panel(self, instance, value):
		if value is None:
			return
		self.bind(on_release=self._create_popup)

	def _set_option(self,option):
		print (option)
		self.value = option
		self.popup.dismiss()

	def _create_popup(self, instance):
		# create the popup
		label = Label(text="1",id='labelvalue')

		def on_value(self,value):
			label.text=str(int(value))

		self.options = "10"
		content = BoxLayout(orientation='vertical', spacing='5dp')
		popup_width = min(0.95 * Window.width, dp(500))
		self.popup = popup = Popup(
		    content=content, title=self.title, size_hint=(None, None),
		    size=(popup_width, '400dp'))
		popup.height = len(self.options) * dp(55) + dp(150)

		content.add_widget(Widget(size_hint_y=None, height=1))
		uid = str(self.uid)
		slider = Slider(min=0,max=100,orientation='horizontal',step=1,value=1)
		slider.bind(value = on_value)

		content.add_widget(slider)
		content.add_widget(label)

		content.add_widget(SettingSpacer())
		btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
		btn.bind(on_release=popup.dismiss)
		btn2 = Button(text='Ok',size_hint_y=None, height=dp(50))

		btn2.bind(on_release=lambda x:self._set_option(label.text))
		content.add_widget(btn)
		content.add_widget(btn2)
		popup.open()



class MySettings(SettingsWithSidebar):
	def __init__(self,*args,**kargs):
		super(MySettings,self).__init__(*args,**kargs)
		Color=(0,0,0,0)
		self.register_type('dynamic_options',SettingDynamicOptions)
		self.register_type('slider',SettingSlider)
