import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.popup import Popup


class BatteryTemp(AnchorLayout):
    pass

class BatteryVolt(AnchorLayout):
    pass

class Regen(AnchorLayout):
    pass

class VehicleSpeed(AnchorLayout):
    pass

class Faults(AnchorLayout):
    pass

class AboutDialog(BoxLayout):
    pass

class DashBar(AnchorLayout):
    def show_about_dialog(self):
        popup = AboutDialog()
        popup_window = Popup(
            title='Phantom Dashboard V1.0.0',
            title_align='center',
            size_hint= (None, None),
            size=(400, 400),
            content=popup)
        popup_window.open()


class Dashboard(AnchorLayout):
    dashSize = ObjectProperty()
    test = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        #Clock.schedule_interval(self.cb, 1/10)


    # def on_touch_down(self, touch):
    #     print(self.parent.size)
    #     print(self.dashSize)

    def cb(self, *largs):
        print('Hello, World')


class DashboardApp(App):
    def build(self):
        print('Building Phantom Dashboard...')
        return Dashboard()


if __name__ == '__main__':
    DashboardApp().run()