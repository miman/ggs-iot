# This lambda function will poll the HC-SR04 distance sensor continously
# It will store that latest value & send it if requested for it
# When this poller is started/stopped it will post a msg to topic "distance/started" or "distance/stopped"
# Requested sensor values will be returned on topic "distance/" + sensor_name + "/value"
# Requests are listened to on MQTT topic "distance/" + sensor_name + "/request"

# Hardware setup:
# Trig to GPIO26
# Echo -> 560 Ohm -> GPIO17 -> 1000 Ohm -> Ground
# VCC to 5V & GND to ground

# Dynamic settings configurable as environment variables:
# DEVICE_NAME: The logical name of the button
# TRIG_PIN_NO: The PIN number of the Trig (Output) connector
# ECHO_PIN_NO: The PIN number of the Echo (Input) connector
# POLL_INTERVAL: The intervall between polls (ms)

# Input: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/ & https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

#Libraries
import logging
import platform
import sys
from threading import Timer
import os
import RPi.GPIO as GPIO
import time
import json
import uuid
import greengrasssdk

# Last read distance value
last_read_distance: int = -1
pins_cache: str = "?"
name_cache: str = "?"

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# The name of this device
device: str = os.environ['AWS_IOT_THING_NAME']

# Posts a message to the value MQTT topic with the given distance
def post_msg(distance):
    global pins_cache
    global device
    global name_cache
    topic_name: str = "distance/" + name_cache + "/value"
    msg = {
        "pins": pins_cache,
        "distanceMm": distance,
        "name": name_cache,
        "type": "DISTANCE_SENSOR",
        "device": device
    }
    print("Sending msg: " + json.dumps(msg))

    try:
        client.publish(
            topic=topic_name,
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

def handle_request(msg):
    print("Distance request msg received: Type: " + str(msg["type"]))
    global last_read_distance
    try:
        # ToDo: handle different request types (one-time, timer & trigger)
        post_msg(last_read_distance)
    except Exception as e:
        logger.error("Failed to handle distance request: " + repr(e))

def update_distance_cache(msg):
    print("Distance value event received: distance: " + str(msg["distanceMm"]))
    global last_read_distance
    global pins_cache
    try:
        # ToDo: handle different request types (one-time, timer & trigger)
        last_read_distance = msg["distanceMm"]
        pins_cache = msg["pins"]
        name_cache = msg["name"]
    except Exception as e:
        logger.error("Failed to handle distance request: " + repr(e))

# This is the Lambda handler, this will be called whenever a msg is received on any topic that is routed to this Lambda
def lambda_handler(event, context):
    print("distance-controller> Msg received")
    # print("power-controller> Msg content: " + json.dumps(event))
    # parse received msg
    topic: str = context.client_context.custom["subject"]

    if "distance/" in topic and "/request" in topic:
        handle_request(event)
    elif "distancepoller/" in topic and "/value" in topic:
        update_distance_cache(event)
    else:
        print("msg received on unknown topic: " + topic)
