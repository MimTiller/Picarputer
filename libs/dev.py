from kivy.app import App
from kivy.uix.camera import Camera

class MainApp(App):
    def build(self):
        cam = Camera(play=True,index=2,resolution=[-1,-1])
        return cam

if __name__== "__main__":
    MainApp().run()
