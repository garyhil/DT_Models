import base64
from datetime import datetime 
import json
import logging
import math
import paho.mqtt.client as mqtt
import random
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT broker configuration
broker_address = "141.47.69.114"
broker_port = 1883
mqtt_topic_human = '/model/d67cf3a3-4441-4191-bf0b-7d5192dd244c/human_detected'

# Function to run the MQTT publisher
def start_publisher():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="Publisher")
    client.connect(host=broker_address, port=broker_port)
    client.loop_start()  # Start the loop to process the background operations
    
    try:
        # Publish a message every 2 seconds
        while True:
            route = {}
            bool = random.choice([True, False])
            message = {
                "route": route,
                "data": bool
            }
            logging.info(f"Human detected: {bool}")
            serialized_message = json.dumps(message)
            encoded_message = base64.b64encode(serialized_message.encode('utf-8'))
            client.publish(mqtt_topic_human, encoded_message)
            time.sleep(2)  # Wait before publishing the next message
    except KeyboardInterrupt:
        logging.info("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
        logging.info("Publisher stopped.")

if __name__ == "__main__":
    start_publisher()
