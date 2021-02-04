import kivy
from kivy_garden.speedmeter import SpeedMeter
kivy.require('1.11.1')

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput

import paho.mqtt.client as mqtt

from threading import Thread
from time import sleep
import json

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

        #Clock.schedule_interval(self.cb, 1/10)

    # def on_touch_down(self, touch):
    #     print(self.parent.size)
    #     print(self.dashSize)

    def cb(self, *largs):
        print('Hello, World')


class DashboardApp(App):
    voltage = NumericProperty(0)  
    temperature = NumericProperty(0)  
    speed = NumericProperty(0)  
    regenValue = NumericProperty(0)  
    regenColor = StringProperty('#00FFFF')        
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
            data = json.loads(msg.payload)

            if topic == MQTT_TOPICS['BATTERY_VOLTAGE_TOPIC']:
                self.setVoltage(data['data'])
                #pass
            elif topic == MQTT_TOPICS['BATTERY_TEMPERATURE_TOPIC']:
                self.setTemperature(data['data'])
                #pass
            elif topic == MQTT_TOPICS['BATTERY_REGEN_TOPIC']:
                self.setRegen(data['data'])
            elif topic == MQTT_TOPICS['VEHICLE_SPEED_TOPIC']:
                self.setSpeed(data['data'])
            elif topic == MQTT_TOPICS['FAULTS_TOPIC']:
                self.setSpeed(data['data'])  
            else:
                print("Invalid topic " + msg.topic)           

        parameters = {'self': self}

        client = mqtt.Client(client_id="kivy-client", clean_session=True, userdata = parameters) # Initialize client
        client.on_connect = on_connect # Call this function when client successfully connects
        client.on_message = on_message # Call this function when message is received on a subscribed topic

        client.connect("localhost", 1883, 60) # Connect to the local MQTT broker

        client.loop_start() # Start the MQTT Client
 
    # Sets the voltage variable in battVolt.kv
    def setVoltage(self, battVolt):
        self.voltage = int(battVolt)

     # Sets the temperature variable in battTemp.kv
    def setTemperature(self, battTemp):
        self.temperature = int(battTemp)

    # Sets the speed variable in vehicleSpeed.kv
    def setSpeed(self, speedValue):
        self.speed = int(speedValue)

    # Sets the regen variable in Regen.kv and the color based on positivity/negativity of regen
    def setRegen(self, regen):
        self.regenValue = float(regen)
        if float(regen) > 0:
            self.regenColor = '#00FFFF'
        else:
            self.regenColor = '#008000'


#backend = backendComms()
if __name__ == "__main__":
    dashboard = DashboardApp().run()