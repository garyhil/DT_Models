import paho.mqtt.client as mqtt
import time
import math
import logging
import threading
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT broker configuration
broker_address = "141.47.69.114"
broker_port = 1883

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="Listener")

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
    """Log and print all incoming MQTT messages."""
    try:
        message_content = msg.payload.decode()  # Decode the payload
        logging.info(f"[{datetime.now()}] New Drying Time: {round(float(message_content), 1)} seconds")
    except ValueError as e:
        logging.error(f"[{datetime.now()}] Error decoding message on topic '{msg.topic}': {e}")

if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the broker
    client.connect(host=broker_address, port=broker_port)

    # Subscribe to all topics
    client.subscribe('/model/98afbba7-754b-45f6-9ef0-6b270c6a21c8/drying_time')  # '#' means subscribe to all topics

    # Start MQTT Client in a separate thread
    mqtt_thread = threading.Thread(target=client.loop_forever)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupt received, stopping...")
        client.loop_stop()  # Stop the MQTT loop
        client.disconnect()  # Disconnect from the broker
