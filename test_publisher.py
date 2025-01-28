import paho.mqtt.client as mqtt
import time
import sys
import math
import random

# MQTT broker configuration
broker_address = "141.47.69.114"
broker_port = 1883
topic_temp = '/model/d67cf3a3-4441-4191-bf0b-7d5192dd244c/human_detected'

def get_new_values():
    temp = random.uniform(a=8.0, b=50.0)
    hum = random.uniform(a=2.0, b=100.0)
    return temp, hum

# Function to run the MQTT publisher
def start_publisher():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="Publisher")
    client.connect(host=broker_address, port=broker_port)
    client.loop_start()  # Start the loop to process the background operations
    
    try:
        # Publish a message every 2 seconds
        while True:
            bool_value = random.choice([True, False])
            print(f"Human Detected: {bool_value}")
            client.publish(topic_temp, str(bool_value))
            time.sleep(2)  # Wait before publishing the next message
    except KeyboardInterrupt:
        print("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
        print("Publisher stopped.")

if __name__ == "__main__":
    start_publisher()
