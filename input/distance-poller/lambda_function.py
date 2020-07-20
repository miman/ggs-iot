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
last_read_distance = -1

ms_between_polls = 0.2

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now
 
#set GPIO Pins
GPIO_TRIGGER = 26
GPIO_ECHO = 17

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# The init function will get the Trig & Echo PIN # from the OS (if not set it will use the default)
# It will then initialize the GPIO PIN's for output/input & settle sensor
def initialize():
    print ("Initializing sensor")
    global ms_between_polls

    # The PIN numbers for this sensor
    trig_pin_no_str: str = os.environ['TRIG_PIN_NO']
    echo_pin_no_str: str = os.environ['ECHO_PIN_NO']
    ms_between_polls_str: str = os.environ['ECHO_PIN_NO']

    if not (trig_pin_no_str is None) and len(trig_pin_no_str) > 0:
        # The Trig sensor pin no was overridden -> set new pin
        GPIO_TRIGGER = int(trig_pin_no_str)
        print("Trigger-PIN was overriden to: " + str(GPIO_TRIGGER))

    if not (echo_pin_no_str is None) and len(echo_pin_no_str) > 0:
        # The Echo sensor pin no was overridden -> set new pin
        GPIO_ECHO = int(echo_pin_no_str)
        print("Echo-PIN was overriden to: " + str(GPIO_ECHO))

    if not (ms_between_polls_str is None) and len(ms_between_polls_str) > 0:
        # The ms_between_polls was overridden -> set new value
        ms_between_polls = int(ms_between_polls_str)
        print("ms between polls was overriden to: " + str(ms_between_polls))

    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Now settle sensor before starting    
    GPIO.output(GPIO_TRIGGER, False)
    print ("Waiting for sensor to settle")
    time.sleep(1)
    
    GPIO.output(GPIO_TRIGGER, True)

# The get_distance fn will get the current distance to an object before the HC-SR04 distance sensor
# The returned distance is in mm
def get_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    start_time = time.time()
    stop_time = time.time()
 
    # save start_time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
 
    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    get_distance = (time_elapsed * 34300) / 2
 
    return (get_distance*10)

# The name of this device
device = os.environ['AWS_IOT_THING_NAME']

# The system name of the RFID reader we are polling (so we can separate events between multiple readers)
sensor_name: str = os.environ['DEVICE_NAME']
if sensor_name is None or len(sensor_name) == 0:
    # No sensor name was supplied -> create a random one
    sensor_name = uuid.uuid1()
    print("Random sensor name was generated: " + sensor_name)

# If the button currently is clicked or not
isOn=False
# The last state of the button that was read
lastState=False

# Posts a message to the value MQTT topic with the given distance
def post_msg(distance):
    text_to_send: str = "Distance read '" + str(distance) + "' on Greengrass device: " + device
    print(text_to_send)
    topic_name: str = ""
    topic_name = "distance/" + sensor_name + "/value"
    msg = {
        "pins": "Trig_" + str(GPIO_TRIGGER) + ":Echo_" + str(GPIO_ECHO),
        "distanceMm": distance,
        "sensorName": sensor_name,
        "sensorType": "Distance",
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

# Post that this Lambda's active state was changed (started/stopped) to the MQTT topic "distance/started" or "distance/stopped"
def post_lambda_state_change(state: str):
    topic_name: str = "distance/" + sensor_name + "/" + state
    print("Sending Distance poller started event on topic: " + topic_name)
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
    global last_read_distance
    global ms_between_polls
    print("Starting Distance poller on PINs (Trig, Echo): (" + str(GPIO_TRIGGER) + ", " + str(GPIO_ECHO) + ")")
    try:
        initialize()
        post_lambda_state_change("started")
        while True:
            last_read_distance = get_distance()
            print ("Measured Distance = %.1f mm" % last_read_distance)
            time.sleep(ms_between_polls)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    finally:
        post_lambda_state_change("stopped")
        GPIO.cleanup()
        print("Closing Distance sensor reader (Trig, Echo): (" + str(GPIO_TRIGGER) + ", " + str(GPIO_ECHO) + ")")

# Start executing the function above
start_read_cycle()

def handle_request(msg):
    print("Distance request msg received: Type: " + str(msg["type"]))
    try:
        # ToDo: handle different request types (one-time, timer & trigger)
        post_msg(last_read_distance)
    except Exception as e:
        logger.error("Failed to handle distance request: " + repr(e))

# This is the Lambda handler, this will be called whenever a msg is received on any topic that is routed to this Lambda
def lambda_handler(event, context):
    print("distance-controller> Msg received")
    # print("power-controller> Msg content: " + json.dumps(event))
    # parse received msg
    topic = context.client_context.custom["subject"]

    if "distance/" in topic and "/request" in topic:
        handle_request(event)
    else:
        print("msg received on unknown topic: " + topic)
