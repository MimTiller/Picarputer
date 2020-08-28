from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class testapp(App):
	def build(self):
		return self.menu()

	def menu(self):
		grid = GridLayout(cols=1,spacing='2dp',size_hint_y=None)
		content = ScrollView(size=(200,500))
		grid.bind(minimum_height=content.setter('height'))
		grid.height = 1500
		self.options = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5]
		for option in self.options:
			btn = Button(text=str(option), size_hint_y=None,height=50)
			grid.add_widget(btn)

		content.add_widget(grid)
		menu_sc = BoxLayout()
		menu_sc.add_widget(content)
		return menu_sc

testapp().run()
