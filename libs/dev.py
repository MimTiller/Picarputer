from kivy.app import App
from kivy.garden.cefpython import CEFBrowser

class SimpleBrowserApp(App):
    def build(self):
        return CEFBrowser(url="http://kivy.org")
SimpleBrowserApp().run()
