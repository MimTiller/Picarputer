
import kivy
kivy.require('1.8.1')

from kivy.app import App
from kivy.lang import Builder

root = Builder.load_string('''
<Separator@Widget>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
<HSeparator@Separator>:
    size_hint_y: None
    height: dp(2)
<VSeparator@Separator>:
    size_hint_x: None
    width: dp(2)
BoxLayout:
    Widget
    VSeparator
    Widget
    VSeparator
    BoxLayout:
        orientation: 'vertical'
        Widget
        HSeparator
        Widget
        HSeparator
        Widget
''')

class TestApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    TestApp().run()
