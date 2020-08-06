# This lambda function will control the servo based on input on the topic "servo/.../set"
# If we get a msg on topic "servo/.../set" we will set the servo to the given angle
#
# We assume the Power relay is on PIN GPIO4

# When the servo is moved an event is sent on "servo/.../moved"

import logging
import platform
import sys
from threading import Timer
import RPi.GPIO as GPIO
from time import sleep
import json
import uuid
import greengrasssdk
import os

# Standard settings
servo_min = 2
servo_max = 12
SERVO_STOP = 0
servo_pin = 4

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

# Function used to get the environment variable with the given name
def gen_env_variable(name, default):
    value: str = os.environ[name]
    if value is None or len(value) == 0:
        # No env variable with given name exists -> use default
        value = default
        print("Env variable with name " + name + " doesn't exist -> using default: " + value)

# The name of this device
device: str = os.environ['AWS_IOT_THING_NAME']
# The system name of the powerdevice we are controlling (so we can separate events between multiple controllers)
actuator_name: str = gen_env_variable('DEVICE_NAME', uuid.uuid1())

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now

# The PIN number for this servo
try:
    io_pin_no_str: str = os.environ['IO_PIN_NO']
except Exception as e:
    # IO PIN # was not supplied
    print("IO PIN # was not supplied")
    # The sensor pin no was overridden -> set new pin
    servo_pin = int(io_pin_no_str)
    print("Power relay PIN was overriden to: " + str(servo_pin))

GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)    # 50 = 50Hz pulse

# Start PWM running, but with value off 0 (pulse off)
servo.start(0)

def move_servo_to_angle(angle):
    global servo
    global servo_min
    global SERVO_STOP
    print("Move servo to angle: " + str(angle))
    print("Rotating...")
    try:
        servo.ChangeDutyCycle(servo_min + (int(angle)/18))
        sleep(0.7)
        servo.ChangeDutyCycle(SERVO_STOP)
    finally:
        print("Rotate completed")
#        servo.stop()

# The handler for a set request, will parse the msg and move the servo to the given angle
def set_msg_received(msg):
    print("Set MQTT msg received")
    try:
        move_servo_to_angle(msg["angle"])
    except Exception as e:
        logger.error("Failed to handle set request")    #  + repr(e)

# Post that this module Lambda active state was changed (started/stopped) to the MQTT topic "servo/.../started" or "servo/.../stopped"
def post_state_change(state: str):
    print("Sending Servo controller state change event on MQTT topic: " + state)
    topic_name: str = "servo/" + actuator_name + "/" + state
    msg = {
        "name": actuator_name,
        "type": "SERVO",
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
    # print("servo-controller> Msg received")
    print("servo-controller> Msg content: " + json.dumps(event))
    # parse received msg
    topic = context.client_context.custom["subject"]
    if "servo/" in topic and "/set" in topic:
        set_msg_received(event)
    else:
        print("msg received on unknown topic: " + topic)

