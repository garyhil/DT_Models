import paho.mqtt.client as mqtt
import threading
import time
import math
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
mqtt_topic_human = '/model/d67cf3a3-4441-4191-bf0b-7d5192dd244c/human_detected'
mqtt_topic_speed = '/model/d67cf3a3-4441-4191-bf0b-7d5192dd244c/speed'
mqtt_broker = '141.47.69.114'  # Update as needed
mqtt_port = 1883  # Update as needed


bool_value = False
max_cartesian_speed = 3  # Maximum speed of the robot arm in m/s
speed = 0.0

# Callback on connection
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logging.info("Successfully connected Client to Broker!")
    else:
        logging.error("Error connecting Client to Broker!")


# Callback on disconnecti
def on_disconnect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logging.info("Successfully disconnected Client from Broker!")
    else:
        logging.error("Error disconnecting Client from Broker!")


# Callback when a message is received
def on_message(client, userdata, message):
    try:
        # Decode the message payload
        bool_value = message.payload.decode('utf-8').lower() == 'true'
        
        # Determine the speed based on the Boolean value
        speed = calculate_speed(bool_value)
        
        # Publish the speed to the output topic
        client.publish(mqtt_topic_speed, speed)
        logging.info(f"New speed send: {round(speed, 1)} m/s")

    except Exception as e:
        logging.info(f"Error processing message: {e}")

# Set up the MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="SpeedController")
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the broker and subscribe to the input topic
client.connect(host=mqtt_broker, port=mqtt_port)
client.subscribe(mqtt_topic_human)

# Start MQTT Client in a separate thread
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

def calculate_speed(human_detected):
    if human_detected:
        speed = 0.3 * max_cartesian_speed
    else:
        speed = 0.8 * max_cartesian_speed
    return speed

def run_simulation():
    global speed

    step_size = 1  # Simulation step size in seconds

    try:
        while True:
            time.sleep(step_size)

    except KeyboardInterrupt:
        logging.info("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the MQTT loop
        client.disconnect()  # Disconnect from the broker
        logging.info("Simulation stopped.")

if __name__ == '__main__':
    run_simulation()