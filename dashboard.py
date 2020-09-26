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

import paho.mqtt.client as mqtt

from threading import Thread
from time import sleep

class backendComms():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("localhost", 1883, 60)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("events/batteryVoltage")
        self.client.subscribe("events/batteryTemperature")
        self.client.subscribe("events/vehicleSpeed")
        self.client.subscribe("events/regen")
        self.client.subscribe("events/faults")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload)) 
        dashboard.setSpeed(msg)  

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
    speed = StringProperty()        
    def build(self):
        print('Building Phantom Dashboard...')
        return Dashboard()

    def on_start(self):
        
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("events/batteryVoltage")
            client.subscribe("events/batteryTemperature")
            client.subscribe("events/vehicleSpeed")
            client.subscribe("events/regen")
            client.subscribe("events/faults")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload)) 
            self.setSpeed(msg.payload.decode('utf-8')) 

        parameters = {'self': self}

        client = mqtt.Client(client_id="kivy-client", clean_session=True, userdata = parameters)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", 1883, 60)

        client.loop_start()

    def setSpeed(self, speed):
        self.speed = speed


#backend = backendComms()
if __name__ == "__main__":
    dashboard = DashboardApp().run()