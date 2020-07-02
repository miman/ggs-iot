# This lambda function will control the relay based on input on the topic "rfid/read" & "btn/state"
#
# If we get a msg on topic "rfid/read" we will activate the power
# If we get a msg on topic "btn/on" we will de-activate the power
#
# We assume the Power relay is on PIN GPIO12
# We assume the LED is on PIN GPIO13

# When the relay is activated/deactivated an event is sent on "pwrRelay/on" or "pwrRelay/off"

import logging
import platform
import sys
from threading import Timer
import RPi.GPIO as GPIO
from time import sleep
import json
import greengrasssdk
import os

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# The name of this device
device: str = os.environ['AWS_IOT_THING_NAME']
# The system name of the powerdevice we are controlling (so we can separate events between multiple controllers)
controlled_device_name: str = os.environ['DEVICE_NAME']

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now

PWR_RELAY_PIN=12
GPIO.setup(PWR_RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)

LEDPIN=13
GPIO.setup(LEDPIN, GPIO.OUT, initial=GPIO.LOW)

def rfid_msg_received(msg):
    print("RFID msg received: Tag-Id: " + str(msg["id"]))
    try:
        GPIO.output(LEDPIN, GPIO.HIGH) # Turn on
        GPIO.output(PWR_RELAY_PIN, GPIO.LOW) # Turn on
        post_state_change("on")
    except Exception as e:
        logger.error("Failed to handle RFID msg: " + repr(e))

def btn_msg_received(msg):
    print("Button msg received")
    try:
        GPIO.output(LEDPIN, GPIO.LOW) # Turn on
        GPIO.output(PWR_RELAY_PIN, GPIO.HIGH) # Turn on
        post_state_change("off")
    except Exception as e:
        logger.error("Failed to handle btn msg: " + repr(e))

# Post that this RFID reader Lambda active state was changed (started/stopped) to the MQTT topic "rfid/started" or "rfid/stopped"
def post_state_change(state: str):
    print("Sending Power controller state change event on MQTT topic: " + state)
    topic_name: str = "pwrRelay/" + state
    msg = {
        "deviceName": controlled_device_name,
        "device": device,
        "state": state
    }
    try:
        client.publish(
            topic=topic_name,
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

# This is the Lambda handler, this will be called whenever a msg is received on any topic that is routed to this Lambda
def lambda_handler(event, context):
    print("power-controller> Msg received")
    # print("power-controller> Msg content: " + json.dumps(event))
    # parse received msg
    topic = context.client_context.custom["subject"]
    if topic == "rfid/read":
        rfid_msg_received(event)
    elif topic == "btn/on":
        btn_msg_received(event)
    else:
        print("msg received on unknown topic: " + topic)
