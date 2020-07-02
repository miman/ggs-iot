# This lambda function will poll the RFID reader & Button continously
# If the button is pressed, it will post msg to topic "btn/on" or "btn/off"
# When this poller is started/stopped it will post a msg to topic "btn/started" or "btn/stopped"

import logging
import platform
import sys
from threading import Timer
import os
import RPi.GPIO as GPIO
from time import sleep
import json
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")

BTN_PIN=19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# The name of this device
device = os.environ['AWS_IOT_THING_NAME']

# The system name of the RFID reader we are polling (so we can separate events between multiple readers)
btn_name: str = os.environ['DEVICE_NAME']

# If the button currently is clicked or not
isOn=False
# The last state of the button that was read
lastState=False

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def lambda_handler(event, context):
    return

def btn_pressed():
    global isOn
    global lastState
    lastState=isOn
    isOn=True
    if lastState != isOn:
      print("Button was pressed")
      post_msg(True)

def btn_released():
    global isOn
    global lastState
    lastState=isOn
    isOn=False
    if lastState != isOn:
      print("Button was released")  
      post_msg(False)

def post_msg(btn_state):
    text_to_send: str = "Button state read '" + str(btn_state) + "' on Greengrass device: " + device
    print(text_to_send)
    topic_name: str = ""
    if btn_state:
        topic_name = "btn/on"
    else:
        topic_name = "btn/off"
    msg = {
        "pin": str(BTN_PIN),
        "state": str(btn_state),
        "btnName": btn_name,
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

# Post that this Lambda's active state was changed (started/stopped) to the MQTT topic "btn/started" or "btn/stopped"
def post_lambda_state_change(topic: str):
    print("Sending RFID reader started event on MQTT")
    msg = {
        "btnName": btn_name,
        "device": device
    }
    try:
        client.publish(
            topic=topic,
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

def start_read_cycle():
    print("Starting Button reader on PIN " + str(BTN_PIN))
    try:
        post_lambda_state_change("btn/started")
        while True:
            btn_state = GPIO.input(BTN_PIN)
            if btn_state == False:
                btn_pressed()
            else:
                btn_released()
            sleep(0.2) # Sleep for 0.2 second

    except Exception as e:
        print("Button reader error: " + str(e))
    finally:
        post_lambda_state_change("btn/stopped")
        print("Closing Button reader (PIN: " + str(BTN_PIN) + ")")

# Start executing the function above
start_read_cycle()
