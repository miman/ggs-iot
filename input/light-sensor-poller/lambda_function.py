# This lambda function will poll the light-sensor continously
# When a new value is retreived, it will post msg to topic "light_sensor/value"
# When this poller is started/stopped it will post a msg to topic "light_sensor/started" or "light_sensor/stopped"

# Dynamic settings configurable as environment variables:
# IO_PIN_NO: The PIN the sensor uses
# DEVICE_NAME: The logical name of the sensor

import logging
import platform
import sys
from threading import Timer
import os
import RPi.GPIO as GPIO
import time
from time import sleep
import json
import uuid
import greengrasssdk

# The sensitivity of this light sensor
sensitivity = 10000
# The PIN of the light sensor
SENSOR_PIN: int = 6
# How long time there is between the polls
polling_time: int = 1
# The last known value, so we don't send the same value all the time
last_value = -1

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now

# The PIN number for this sensor
io_pin_no_str: str = os.environ['IO_PIN_NO']

if not (io_pin_no_str is None) and len(io_pin_no_str) > 0:
    # The sensor pin no was overridden -> set new pin
    SENSOR_PIN = int(io_pin_no_str)
    print("Sensor-PIN was overriden to: " + str(SENSOR_PIN))

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
      post_state_msg(True)

def is_inactive():
    global isOn
    global lastState
    lastState=isOn
    isOn=False
    if lastState != isOn:
      print("Sensor is in-active")  
      post_state_msg(False)

def post_state_msg(sensor_state):
    text_to_send: str = "Sending active state '" + str(sensor_state) + "' for Greengrass device: " + device
    print(text_to_send)
    topic_name: str = ""
    if sensor_state:
        topic_name = "light_sensor/" + sensor_name + "/on"
    else:
        topic_name = "light_sensor/" + sensor_name + "/off"
    msg = {
        "pin": str(SENSOR_PIN),
        "state": str(sensor_state),
        "sensorName": sensor_name,
        "sensorType": "LIGHT_SENSOR",
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
def post_sensor_value(value: str):
    topic_name: str = "light_sensor/" + sensor_name + "/value"
    print("Sending sensor value event on topic: " + topic_name)
    msg = {
        "sensorName": sensor_name,
        "device": device,
        "value": value
    }
    try:
        client.publish(
            topic=topic_name,
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

# Infinite runner function
# Polls for new sensor values
def start_read_cycle():
    print("Starting sensor poller on PIN " + str(SENSOR_PIN))
    try:
        post_sensor_value("started")
        while True:
            # Clear capacitor
            GPIO.setup(SENSOR_PIN, GPIO.OUT)
            GPIO.output(SENSOR_PIN, GPIO.LOW)
            time.sleep(0.1)
            
            # Activate PIN
            GPIO.setup(SENSOR_PIN, GPIO.IN)
            current_time = time.time()
            diff = 0
            
            # measure how long time it takes to fill the capacitor
            while(GPIO.input(SENSOR_PIN) == GPIO.LOW):
                diff = time.time() - current_time

            # We now have a light sensor value            
            print("Light sensor value: " + diff*sensitivity)
            if (last_value != diff):
                post_sensor_value(diff*sensitivity)
                last_value = diff
            # Wait some time before polling again
            time.sleep(polling_time)

    except Exception as e:
        print("Light sensor reader error: " + str(e))
    finally:
        post_sensor_value("stopped")
        print("Closing sensor poller (PIN: " + str(SENSOR_PIN) + ")")

# Start executing the function above
start_read_cycle()
