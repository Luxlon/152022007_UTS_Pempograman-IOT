import paho.mqtt.client as mqtt
import json

# MQTT Broker settings
broker = 'broker.emqx.io'
port = 1883
mqtt_topic = 'UTS_IOT/emqx/esp32'
username = 'parisafauzan'
password = 'paris364'

# Callback function when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(mqtt_topic)
    else:
        print(f"Failed to connect, return code {rc}")

# Callback function when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Message received on topic '{msg.topic}': {payload}")
        
        # Parsing payload (assuming JSON format)
        data = json.loads(payload)
        
        # Example: Print parsed data
        print("Parsed Data:")
        for key, value in data.items():
            print(f"{key}: {value}")
    except json.JSONDecodeError:
        print("Error decoding JSON")

# Create an MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(username, password)

# Attach callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, keepalive=60)

# Start the loop to process callbacks
client.loop_forever()