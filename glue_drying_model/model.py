import base64
from datetime import datetime
import logging
import json
import math
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
mqtt_topic_temp = '/model/98afbba7-754b-45f6-9ef0-6b270c6a21c8/temperature'
mqtt_topic_hum = '/model/98afbba7-754b-45f6-9ef0-6b270c6a21c8/humidity'
mqtt_topic_time = '/model/98afbba7-754b-45f6-9ef0-6b270c6a21c8/drying_time'
mqtt_broker = '141.47.69.114'  # Update as needed
mqtt_port = 1883  # Update as needed

temp = None  # Last received temperature value
hum = None   # Last received humidity value
new_data_received = False  # Flag to track if new data was received

# Callback on connection
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logging.info("Successfully connected Client to Broker!")
    else:
        logging.error("Error connecting Client to Broker!")

# Callback on disconnect
def on_disconnect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logging.info("Successfully disconnected Client from Broker!")
    else:
        logging.error("Error disconnecting Client from Broker!")

# Callback for MQTT messages
def on_message(client, userdata, msg):
    global temp, hum, new_data_received
    try:
        if msg.topic == mqtt_topic_temp:
            decoded_msg = base64.b64decode(msg.payload).decode('utf-8')
            deserialize_msg = json.loads(decoded_msg)
            temp = deserialize_msg.get("data")
            logging.info(f'New Temperature Value Received: {round(temp, 1)} °C')
        elif msg.topic == mqtt_topic_hum:
            decoded_msg = base64.b64decode(msg.payload).decode('utf-8')
            deserialize_msg = json.loads(decoded_msg)
            hum = deserialize_msg.get("data")            
            logging.info(f'New Humidity Value Received: {round(hum, 0)} %')
        
        # Calculate and publish the optimal glue evaporation time if both temp and hum are received
        if temp is not None and hum is not None:
            evaporation_time = calculate_optimal_glue_evaporation_time(temp, hum)
            client.publish(mqtt_topic_time, evaporation_time)
            logging.info(f'Optimal Glue Evaporation Time: {round(evaporation_time, 1)} seconds')
    except ValueError:
        logging.error('Error converting MQTT value')

def on_publish(client, userdata, mid):
    logging.info(f"Published message with mid: {mid}")

# MQTT Client Setup
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="GlueController")
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic_temp)
client.subscribe(mqtt_topic_hum)

def calculate_humidity_part(humidity):
    """Calculate the humidity part based on the equation."""
    return 5.0 + 10.0 / (-1.0 - math.exp(0.1 * humidity - 4.0))

def calculate_temperature_part(temperature):
    """Calculate the temperature part based on the equation."""
    return 10.0 + 20.0 / (1.0 + math.exp(0.13 * temperature - 4.0))

def calculate_optimal_glue_evaporation_time(temp, hum):
    """Calculate the optimal glue evaporation time."""
    humidity_part = calculate_humidity_part(hum)
    temperature_part = calculate_temperature_part(temp)
    return humidity_part + temperature_part

if __name__ == '__main__':
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logging.info("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the MQTT loop
        client.disconnect()  # Disconnect from the broker
        logging.info("Simulation stopped.")
