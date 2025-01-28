import paho.mqtt.client as mqtt
import time
import sys
import math
import random

# MQTT broker configuration
broker_address = "141.47.69.114"
broker_port = 1883
topic_temp = '/model/570c5583-8e04-487b-a490-601e62f2f812/renewable_energy'

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
            energy_kW = random.uniform(a=0.0, b=100.0)
            print(f"Current energy production: {round(energy_kW,1)} kW")
            client.publish(topic_temp, str(energy_kW))
            time.sleep(2)  # Wait before publishing the next message
    except KeyboardInterrupt:
        print("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
        print("Publisher stopped.")

if __name__ == "__main__":
    start_publisher()
