# This lambda function will poll the PIR sensor continously
# If the sensor is active/inavctive, it will post msg to topic "pir/on" or "pir/off"
# When this poller is started/stopped it will post a msg to topic "pir/started" or "pir/stopped"

# Dynamic settings configurable as environment variables:
# IO_PIN_NO: The PIN the sensor uses
# DEVICE_NAME: The logical name of the sensor

import logging
import platform
import sys
from threading import Timer
import os
import RPi.GPIO as GPIO
from time import sleep
import json
import uuid
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now

# The PIN number for this sensor
io_pin_no_str: str = os.environ['IO_PIN_NO']

SENSOR_PIN: int = 20
if not (io_pin_no_str is None) and len(io_pin_no_str) > 0:
    # The sensor pin no was overridden -> set new pin
    SENSOR_PIN = int(io_pin_no_str)
    print("Sensor-PIN was overriden to: " + str(SENSOR_PIN))

GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The name of this device
device = os.environ['AWS_IOT_THING_NAME']

# The system name of the sensor we are polling (so we can separate events between multiple readers)
sensor_name: str = os.environ['DEVICE_NAME']
if sensor_name is None or len(sensor_name) == 0:
    # No sensor name was supplied -> create a random one
    sensor_name = uuid.uuid1()
    print("Random sensor name was generated: " + sensor_name)

# If the button currently is clicked or not
isOn=False
# The last state of the button that was read
lastState=False

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def lambda_handler(event, context):
    return

def is_active():
    global isOn
    global lastState
    lastState=isOn
    isOn=True
    if lastState != isOn:
      print("Sensor is active")
      post_msg(True)

def is_inactive():
    global isOn
    global lastState
    lastState=isOn
    isOn=False
    if lastState != isOn:
      print("Sensor is in-active")  
      post_msg(False)

def post_msg(btn_state):
    text_to_send: str = "Read sensor state '" + str(btn_state) + "' on Greengrass device: " + device
    print(text_to_send)
    topic_name: str = ""
    if btn_state:
        topic_name = "pir/" + sensor_name + "/on"
    else:
        topic_name = "pir/" + sensor_name + "/off"
    msg = {
        "pin": str(SENSOR_PIN),
        "state": str(btn_state),
        "sensorName": sensor_name,
        "sensorType": "PIR",
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

# Post that this Lambda's active state was changed (started/stopped) to the MQTT topic "pir/started" or "pir/stopped"
def post_lambda_state_change(state: str):
    topic_name: str = "pir/" + sensor_name + "/" + state
    print("Sending sensor poller started event on topic: " + topic_name)
    msg = {
        "sensorName": sensor_name,
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

def start_read_cycle():
    print("Starting sensor poller on PIN " + str(SENSOR_PIN))
    try:
        post_lambda_state_change("started")
        while True:
            btn_state = GPIO.input(SENSOR_PIN)
            if btn_state == False:
                is_active()
            else:
                is_inactive()
            sleep(0.2) # Sleep for 0.2 second

    except Exception as e:
        print("PIR reader error: " + str(e))
    finally:
        post_lambda_state_change("stopped")
        print("Closing sensor poller (PIN: " + str(SENSOR_PIN) + ")")

# Start executing the function above
start_read_cycle()
