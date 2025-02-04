import paho.mqtt.client as mqtt
import threading
import time
import logging
from datetime import datetime 
import base64
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
mqtt_topic_energy = '/model/570c5583-8e04-487b-a490-601e62f2f812/renewable_energy'
mqtt_topic_mode = '/model/570c5583-8e04-487b-a490-601e62f2f812/operation_mode'
mqtt_broker = '141.47.69.114'  # Update as needed
mqtt_port = 1883  # Update as needed

# Energy thresholds (in kW)
NO_PRODUCTION_THRESHOLD = 10  # kW
ENERGY_SAVING_THRESHOLD = 50  # kW


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
        decoded_payload = base64.b64decode(message.payload).decode('utf-8')
        deserializes_message = json.loads(decoded_payload)
        energy_kW = deserializes_message.get("data", {})
        logging.info(f"Received energy input: {energy_kW} kW")

        # Determine the operating mode
        mode = determine_mode(energy_kW)

        # Publish the operating mode to the output topic
        client.publish(mqtt_topic_mode, mode)
        logging.info(f"Published mode: {mode}")

    except ValueError as e:
        logging.error(f"Invalid energy input received: {message.payload.decode('utf-8')}. Error: {e}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def determine_mode(energy_kW):
    """
    Determine operating mode based on current energy production in kW.

    Args:
        energy_kW (float): Current energy production in kW.

    Returns:
        int: 0 (no production), 1 (energy-saving production), or 2 (full production).
    """
    if energy_kW <= NO_PRODUCTION_THRESHOLD:
        return 0  # No production
    elif energy_kW < ENERGY_SAVING_THRESHOLD:
        return 1  # Energy-saving production
    else:
        return 2  # Full production
    
# Set up the MQTT client
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="EnergyModeSelector")
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the broker
client.connect(host=mqtt_broker, port=mqtt_port)
client.subscribe(mqtt_topic_energy)

# Start MQTT Client in a separate thread
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

def run_simulation():
    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        logging.info("Interrupt (CTRL+C) received, shutting down...")
    finally:
        client.loop_stop()  # Stop the MQTT loop
        client.disconnect()  # Disconnect from the broker
        logging.info("Simulation stopped.")

if __name__ == '__main__':
    run_simulation()
