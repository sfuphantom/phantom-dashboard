import paho.mqtt.client as mqtt
import json
import time

from query import insertRecord

# Front-end communication topics
MQTT_PUB_TOPICS = {
    "BATTERY_VOLTAGE_TOPIC": "events/batteryVoltage",
    "BATTERY_TEMPERATURE_TOPIC": "events/batteryTemperature",
    "VEHICLE_SPEED_TOPIC": "events/vehicleSpeed",
    "BATTERY_REGEN_TOPIC": "events/batteryRegen",
    "FAULTS_TOPIC": "events/faults",
}

# VCU/BMS simulation topics
MQTT_SIM_SUB_TOPICS = {
    "BATTERY_VOLTAGE_TOPIC": "events/batteryVoltageSim",
    "BATTERY_TEMPERATURE_TOPIC": "events/batteryTemperatureSim",
    "VEHICLE_SPEED_TOPIC": "events/vehicleSpeedSim",
    "BATTERY_REGEN_TOPIC": "events/batteryRegenSim",
    "FAULTS_TOPIC": "events/faultsSim",
}

class vehicleCommsManager():
    """
    vehicleCommsManager Class is responsible for communicating between CAN
    from VCU/BMS to front-end over MQTT. Currently messages over CAN are 
    simulated by MQTT topics but this is to be replaced with CAN.
    """
    def __init__(self):
        self.client = mqtt.Client(client_id="vehicleComms", clean_session=True) # Initialize client
        self.client.on_connect = self.on_connect # Call this function when client successfully connects
        self.client.on_message = self.on_message # Call this function when message is received on a subscribed topic
        self.client.on_disconnect = self.on_disconnect
        self.client.connect("localhost", 1883, 60) # Connect to the local MQTT broker

        self.client.loop_start() # Start the MQTT Client        
      
    def on_disconnect(self, client, userdata, rc):
        print("disconnected with result code "+str(rc))

   
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for key in MQTT_SIM_SUB_TOPICS.keys():
            client.subscribe(MQTT_SIM_SUB_TOPICS[key])

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        try:
            print(msg.topic+" "+str(msg.payload)) 
            topic = msg.topic
            data = msg.payload

            if topic == MQTT_SIM_SUB_TOPICS['BATTERY_VOLTAGE_TOPIC']:
                self.setVoltage(data.decode('utf-8'))
            elif topic == MQTT_SIM_SUB_TOPICS['BATTERY_TEMPERATURE_TOPIC']:
                self.setTemperature(data.decode('utf-8'))
            elif topic == MQTT_SIM_SUB_TOPICS['BATTERY_REGEN_TOPIC']:
                self.setRegen(data.decode('utf-8'))
            elif topic == MQTT_SIM_SUB_TOPICS['VEHICLE_SPEED_TOPIC']:
                self.setSpeed(data.decode('utf-8'))
            elif topic == MQTT_SIM_SUB_TOPICS['FAULTS_TOPIC']:
                self.setFaults(data.decode('utf-8'))  
            else:
                print("Invalid topic " + msg.topic)
                  
        except Exception as e:
            print(e)

    # Sends message to front-end to set speed and saves data in database
    def setSpeed(self, speedValue):
        data = json.dumps({'data': speedValue});
        insertRecord('Test Bench', 'Mahmouds Pi', 'Speed Sensor', data)
        self.client.publish(MQTT_PUB_TOPICS['VEHICLE_SPEED_TOPIC'], payload=data, qos=2, retain=False)

    # Sends message to front-end to set regen and saves data in database
    def setRegen(self, regen):
        data = json.dumps({'data': regen});
        insertRecord('Test Bench', 'Mahmouds Pi', 'Regen', data)
        self.client.publish(MQTT_PUB_TOPICS['BATTERY_REGEN_TOPIC'], payload=data, qos=2, retain=False)

    # Sends message to front-end to set voltage and saves data in database
    def setVoltage(self, voltage):
        data = json.dumps({'data': voltage});
        insertRecord('Test Bench', 'Mahmouds Pi', 'BMS Slave', data)
        self.client.publish(MQTT_PUB_TOPICS['BATTERY_VOLTAGE_TOPIC'], payload=data, qos=2, retain=False)

    # Sends message to front-end to set temperature and saves data in database
    def setTemperature(self, temperature):
        data = json.dumps({'data': temperature});
        insertRecord('Test Bench', 'Mahmouds Pi', 'Thermistor Board', data)
        self.client.publish(MQTT_PUB_TOPICS['BATTERY_TEMPERATURE_TOPIC'], payload=data, qos=2, retain=False)

    # Idle process...
    def process(self):
        time.sleep(5)

if __name__ == "__main__":
    commsMgr = vehicleCommsManager()

    print("Process starting...")
    while True:
        commsMgr.process()
