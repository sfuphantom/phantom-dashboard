from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button

class CalcApp(App):
    def build(self):
        layout = GridLayout(cols=10, pos_hint={'center_x':0.3} , size_hint=(None, None))
            # ^ position grid in mid horizontally, ^ make grid use custom
            # size.
        # Bind the size of the gridlayout of to it's minimum_size(calculated
        # by children size)
        layout.bind(minimum_size = layout.setter('size'))
        # bind the top of the grid to it's height'
        layout.bind(height = layout.setter('top'))
        for x in range(0,10):
            for x in range(0,2):
                layout.add_widget(Button(color=(1, 0, 0, 1), size_hint_x=None, width=50))
        return layout

CalcApp().run()