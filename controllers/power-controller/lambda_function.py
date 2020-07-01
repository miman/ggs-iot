# This lambda function will control the relay based on input on the topic "rfid/read" & "btn/state"
# If we get a msg on topic "rfid/read" we will activate the power
# If we get a msg on topic "btn/state" we will de-activate the power

import logging
import platform
import sys
from threading import Timer
import RPi.GPIO as GPIO
from time import sleep
import json
import greengrasssdk

print("power-controller> 1")
# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

print("power-controller> 2")
# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

print("power-controller> 3")
PWR_RELAY_PIN=12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setup(PWR_RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)

print("power-controller> 4")
LEDPIN=13
GPIO.setup(LEDPIN, GPIO.OUT, initial=GPIO.LOW)

print("power-controller> 5")

def rfid_msg_received(msg):
    print("RFID msg received")
    try:
        GPIO.output(LEDPIN, GPIO.HIGH) # Turn on
        GPIO.output(PWR_RELAY_PIN, GPIO.LOW) # Turn on
    except Exception as e:
        logger.error("Failed to handle RFID msg: " + repr(e))

def btn_msg_received(msg):
    print("Button msg received")
    try:
        GPIO.output(LEDPIN, GPIO.LOW) # Turn on
        GPIO.output(PWR_RELAY_PIN, GPIO.HIGH) # Turn on
    except Exception as e:
        logger.error("Failed to handle btn msg: " + repr(e))

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
# context: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
def lambda_handler(event, context):
    print("power-controller> Msg received")
    print("power-controller> context-ARN:" + context.invoked_function_arn)
    print("power-controller> Msg content: " + json.dumps(event))
    print("power-controller> aws_request_id :" + context.aws_request_id )
    print("power-controller> custom :" + json.dumps(context.client_context.custom) )
    # parse received msg
    topic = context.client_context.custom["subject"]
    if topic == "rfid/read":
        rfid_msg_received(event)
    elif topic == "btn/state":
        btn_msg_received(event)
    else:
        print("msg received on unknown topic: " + topic)
