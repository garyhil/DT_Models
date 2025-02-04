import base64
import json
import logging
import math
import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT broker configuration
broker_address = "141.47.69.114"
broker_port = 1883
mqtt_topic_temp = '/model/98afbba7-754b-45f6-9ef0-6b270c6a21c8/temperature'
mqtt_topic_hum = '/model/98afbba7-754b-45f6-9ef0-6b270c6a21c8/humidity'

# Function to run the MQTT publisher
def start_publisher():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="Publisher")
    client.connect(host=broker_address, port=broker_port)
    client.loop_start()  # Start the loop to process the background operations
    
    try:
        # Publish a message every 2 seconds
        while True:
            temp = random.uniform(a=8.0, b=50.0)
            route = {}
            message = {
                "route": route,
                "data": temp
            }
            serialized_message = json.dumps(message)
            encoded_message = base64.b64encode(serialized_message.encode('utf-8'))
            logging.info(f"Temperature: {round(temp,1)} °C")
            client.publish(mqtt_topic_temp, encoded_message)
            time.sleep(2)  # Wait before publishing the next message
            
            hum = random.uniform(a=2.0, b=100.0)
            message = {
                "route": route,
                "data": hum
            }
            serialized_message = json.dumps(message)
            encoded_message = base64.b64encode(serialized_message.encode('utf-8'))
            logging.info(f"Humidity: {round(hum,1)} %")
            client.publish(mqtt_topic_hum, encoded_message)
            time.sleep(2)
    except KeyboardInterrupt:
        logging.info("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
        logging.info("Publisher stopped.")

if __name__ == "__main__":
    start_publisher()
