# This lambda function will poll the RFID reader continously
# If the rfid-tag is read, it will post msg to topic "rfid/read"

import logging
import platform
import sys
from threading import Timer
import os
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import json
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Initiate RFID reader
reader = SimpleMFRC522()

device = os.environ['AWS_IOT_THING_NAME']

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def lambda_handler(event, context):
    return

def post_read_rfid_tag(id_no, text):
    text_to_send="RFID tag read '" + str(id_no) + "' with content '" + text.strip() + "' on Greengrass device: " + device
    print(text_to_send)
    msg = {
        "id": id_no,
        "text": text.strip(),
        "device": device
    }
    try:
        client.publish(
            topic="rfid/read",
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

def start_read_cycle():
    print("Starting RFID RC522 reader")
    try:
        while True:
            id_no, text = reader.read()
            post_read_rfid_tag(id_no, text)
            sleep(0.2) # Sleep for 0.2 second

    except Exception as e:
        print("RFID reader error: " + str(e))
    finally:
        print("Closing RFID reader")

# Start executing the function above
start_read_cycle()
