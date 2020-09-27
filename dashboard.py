import kivy
from kivy.garden.gauge import Gauge
kivy.require('1.11.1')

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.popup import Popup

import paho.mqtt.client as mqtt

from threading import Thread
from time import sleep

MQTT_TOPICS = {
    "BATTERY_VOLTAGE_TOPIC": "events/batteryVoltage",
    "BATTERY_TEMPERATURE_TOPIC": "events/batteryTemperature",
    "VEHICLE_SPEED_TOPIC": "events/vehicleSpeed",
    "BATTERY_REGEN_TOPIC": "events/batteryRegen",
    "FAULTS_TOPIC": "events/faults",
}

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
    increasing = NumericProperty(1)
    begin = NumericProperty(50)
    step = NumericProperty(1)
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)

        box = FloatLayout(size_hint=(1, 1))
        self.gauge = Gauge(value=50, size_gauge=256, size_text=24, pos_hint={'x':0.335, 'y':0.25}, size_hint= (1, 1))

        box.add_widget(self.gauge)
        self.add_widget(box)
        #Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.1)
        #Clock.schedule_interval(self.cb, 1/10)

    # def on_touch_down(self, touch):
    #     print(self.parent.size)
    #     print(self.dashSize)

    def cb(self, *largs):
        print('Hello, World')

    def gauge_increment(self):
        begin = self.begin
        begin += self.step * self.increasing
        if begin > 0 and begin < 100:
            self.gauge.value = begin
        else:
            self.increasing *= -1
        self.begin = begin


class DashboardApp(App):
    speed = StringProperty()        
    def build(self):
        #Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.1)
        print('Building Phantom Dashboard...')
        self.dashboard = Dashboard()
        return self.dashboard

    def on_start(self):      
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            for key in MQTT_TOPICS.keys():
                client.subscribe(MQTT_TOPICS[key])

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload)) 
            topic = msg.topic
            data = msg.payload

            if topic == MQTT_TOPICS['BATTERY_VOLTAGE_TOPIC']:
                self.setSpeed(data.decode('utf-8'))
            elif topic == MQTT_TOPICS['BATTERY_TEMPERATURE_TOPIC']:
                self.setSpeed(data.decode('utf-8'))
            elif topic == MQTT_TOPICS['BATTERY_REGEN_TOPIC']:
                self.setSpeed(data.decode('utf-8'))
            elif topic == MQTT_TOPICS['VEHICLE_SPEED_TOPIC']:
                self.setSpeed(data.decode('utf-8'))
            elif topic == MQTT_TOPICS['FAULTS_TOPIC']:
                self.setSpeed(data.decode('utf-8'))  
            else:
                print("Invalid topic " + msg.topic)           

        parameters = {'self': self}

        client = mqtt.Client(client_id="kivy-client", clean_session=True, userdata = parameters)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", 1883, 60)

        client.loop_start()

    def setSpeed(self, speed):
        self.dashboard.gauge.value = int(speed)


#backend = backendComms()
if __name__ == "__main__":
    dashboard = DashboardApp().run()