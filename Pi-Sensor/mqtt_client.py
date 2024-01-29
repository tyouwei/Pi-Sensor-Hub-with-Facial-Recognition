import paho.mqtt.client as mqtt
import json

class MQTTClient:
    def __init__(self):
        # Specify the path to your JSON file
        json_file_path = '/home/admin/Desktop/IoT_Project/SettingsPage/UserPrefs.json'

        # Open the JSON file for reading
        with open(json_file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
        
        broker = data['mqttSettings']['broker']
        port = data['mqttSettings']['port']
        self.topic = data['mqttSettings']['topic']

        self.client = mqtt.Client()
        self.client.on_publish = self.on_publish
        self.client.connect(broker , port, 60)
        self.client.loop_start()

    def on_publish(self, client, userdata, mid):
        print(f"Message published: {mid}")

    def publish_json(self, json_object):
        self.client.publish(self.topic, json.dumps(json_object))
        
    def publish_message(self, message):
        self.client.publish(self.topic, message)
