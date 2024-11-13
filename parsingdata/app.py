from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json

# MQTT Broker settings
broker = 'broker.emqx.io'
port = 1883
mqtt_topic = 'UTS_IOT/emqx/esp32'
username = 'parisafauzan'
password = 'paris364'

# Flask app
app = Flask(__name__)

# Global variable to store parsed data
mqtt_data = []

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
        print("Parsed Data:")
        for key, value in data.items():
            print(f"{key}: {value}")
            
        # Append parsed data to global variable
        mqtt_data.append(data)

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

# Start the loop to process callbacks in a separate thread
def start_mqtt():
    client.loop_start()

# Route to display MQTT data in a table
@app.route('/')
def index():
    return render_template('index.html', mqtt_data=mqtt_data)

if __name__ == '__main__':
    start_mqtt()  # Start MQTT client in background
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run Flask app
