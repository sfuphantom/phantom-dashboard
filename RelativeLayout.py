from kivy.app import App
from kivy.lang import Builder

class Test(App):

    def build(self):
        return Builder.load_string(gui)


Test().run()