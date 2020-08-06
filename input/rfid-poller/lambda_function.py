# This lambda function will poll the RFID reader continously
# If the rfid-tag is read, it will post msg to topic "rfid/read"
# When this rfid reader is started/stopped it will post a msg to topic "rfid/started" or "rfid/stopped"

# Dynamic settings configurable as environment variables:
# DEVICE_NAME: The logical name of the RFID unit

import logging
import platform
import sys
from threading import Timer
import os
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import json
import uuid
import greengrasssdk
from datetime import datetime, timedelta

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Initiate RFID reader
reader = SimpleMFRC522()

# The name of this device
device: str = os.environ['AWS_IOT_THING_NAME']
# The system name of the RFID reader we are polling (so we can separate events between multiple readers)
sensor_name: str = os.environ['DEVICE_NAME']
if sensor_name is None or len(sensor_name) == 0:
    # No sensor name was supplied -> create a random one
    sensor_name = uuid.uuid1()
    print("Random sensor name was generated: " + sensor_name)

# The last time a tag was read
lastReadTime: datetime = datetime(2020, 1, 1, 0, 0)
# The last Tag-Id that was read
lastReadTag: str = ""

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def lambda_handler(event, context):
    return

# Post that a new Tag was read to the MQTT topic "rfid/read"
def post_read_rfid_tag(id_no: str, text: str):
    text_to_send="Read RFID tag '" + str(id_no) + "' with content '" + text.strip() + "' on Greengrass device: " + device
    print(text_to_send)
    msg = {
        "id": id_no,
        "text": text.strip(),
        "name": sensor_name,
        "type": "RFID_READER",
        "device": device
    }
    try:
        client.publish(
            topic="rfid/" + sensor_name + "/read",
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

# Post that this RFID reader Lambda active state was changed (started/stopped) to the MQTT topic "rfid/started" or "rfid/stopped"
def post_rfid_poller_state_change(state: str):
    topic_name: str = "rfid/" + sensor_name + "/" + state
    print("Sending RFID reader started event on topic: " + topic_name)
    msg = {
        "name": sensor_name,
        "type": "RFID_READER",
        "device": device
    }
    try:
        client.publish(
            topic=topic_name,
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

# The main long lived loop function
def start_read_cycle():
    print("Starting RFID RC522 reader")
    global lastReadTime
    global lastReadTag
    try:
        post_rfid_poller_state_change("started")
        while True:
            id_no, text = reader.read()
            now: datetime = datetime.now()
            if id_no != lastReadTag or now > lastReadTime + timedelta(milliseconds=500):
                # it is a new tag or the time sinca last read was more than 500 ms -> count as new read
                lastReadTag = id_no
                post_read_rfid_tag(id_no, text)
            else:
                print("Re-read the same RFID tag: " + str(id_no) + ", with text: " + text)
            lastReadTime = now
            sleep(0.2) # Sleep for 0.2 second

    except Exception as e:
        print("RFID reader error: " + str(e))
    finally:
        post_rfid_poller_state_change("stopped")
        print("Closing RFID reader")

# Start executing the long-lived polling-function
start_read_cycle()
