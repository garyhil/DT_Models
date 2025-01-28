import paho.mqtt.client as mqtt
import time
import sys
import math
import random

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
            hum = random.uniform(a=2.0, b=100.0)
            print(f"Temperature: {round(temp,1)} °C, Humidity: {round(hum,1)} %")
            client.publish(mqtt_topic_temp, payload=f"{round(temp,1)}", qos=1)
            client.publish(mqtt_topic_hum, payload=f"{round(hum,1)}", qos=1)
            time.sleep(2)  # Wait before publishing the next message
    except KeyboardInterrupt:
        print("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
        print("Publisher stopped.")

if __name__ == "__main__":
    start_publisher()
