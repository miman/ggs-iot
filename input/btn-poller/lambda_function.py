# This lambda function will poll the RFID reader & Button continously
# If the button is pressed, it will post msg to topic "btn/state"

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

device = os.environ['AWS_IOT_THING_NAME']

isOn=False
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

def post_msg(btn_state):
    text_to_send="Button state read '" + str(btn_state) + "' on Greengrass device: " + device
    print(text_to_send)
    msg = {
        "pin": str(BTN_PIN),
        "state": str(btn_state),
        "device": device
    }
    try:
        client.publish(
            topic="btn/state",
            queueFullPolicy="AllOrException",
            payload=json.dumps(msg)
        )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

def start_read_cycle():
    print("Starting Button reader on PIN " + str(BTN_PIN))
    try:
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
        print("Closing Button reader (PIN: " + str(BTN_PIN) + ")")

# Start executing the function above
start_read_cycle()
