# This lambda function will poll the water-sensor continously
# When a new value is retreived, it will post msg to topic "water_sensor/value"
# When this poller is started/stopped it will post a msg to topic "water_sensor/started" or "water_sensor/stopped"
# It uses the MCP3008 ADC (Analog-Digital converter to convert the analog signal (voltage) into a digital value)

# Dynamic settings configurable as environment variables:
# IO_PIN_NO: The PIN the sensor uses
# DEVICE_NAME: The logical name of the sensor

import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import logging
import platform
import sys
from threading import Timer
import os
import time
from time import sleep
import json
import uuid
import greengrasssdk

# This function is used to seup the SPI bus connecting to the MOSI/MISO PIN's on the Raspberry PI
def spio_setup():
    global channel0
    # Create the SPI BUS
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # Create the cs (Chip Select)
    cs = digitalio.DigitalInOut(board.D5)

    # Create the MCP object
    mcp = MCP.MCP3008(spi, cs)

    # Create the analog input channel on PIN 0 on the MCP3008 chip
    channel0 = AnalogIn(mcp, MCP.P0)

# The sensitivity of this water sensor
sensitivity = 10000
# The PIN of the water sensor
SENSOR_PIN: int = 22
# How long time there is between the polls
polling_time: int = 1
# The last known value, so we don't send the same value all the time
last_value = -1
last_detected_value = False

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

GPIO.setup(SENSOR_PIN, GPIO.IN)

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

def post_state_msg(sensor_state):
    text_to_send: str = "Sending active state '" + str(sensor_state) + "' for Greengrass device: " + device
    print(text_to_send)
    topic_name: str = "water_sensor/" + sensor_name + "/" + sensor_state
    msg = {
        "pin": str(SENSOR_PIN),
        "state": str(sensor_state),
        "name": sensor_name,
        "type": "WATER_SENSOR",
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
def post_sensor_value(value: int, water_detected: bool):
    global last_value
    global last_detected_value
    if last_value == value and last_detected_value == water_detected:
        print("Water-sensor> Value hasn't changed -> we don't send an update")
        return

    # Remeber last sent values
    last_value = value
    last_detected_value = water_detected

    # Send the values on MQTT
    topic_name: str = "water_sensor/" + sensor_name + "/value"
    print("Sending sensor value event on topic: " + topic_name)
    msg = {
        "name": sensor_name,
        "type": "WATER_SENSOR",
        "device": device,
        "value": value,
        "waterDetected": water_detected
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
    global channel0
    global last_value
    global SENSOR_PIN
    global sensitivity
    global polling_time
    print("Starting sensor poller on PIN " + str(SENSOR_PIN))
    try:
        post_state_msg("started")
        while True:
            # Print the analog value
            print('ADC Value: ', channel0.value)
        #   print('ADC Voltage: ', str(chan.voltage) + 'V')
        
            # Print the digital value
            water_detected = GPIO.input(SENSOR_PIN)
            if water_detected == 0:
                water_bool = 'true'
            else:
                water_bool = 'false'
            print('Water detected: ', water_bool)

            post_sensor_value(channel0.value, water_detected == 0)
            # Wait some time before polling again
            time.sleep(polling_time)

    except Exception as e:
        print("water sensor reader error: " + str(e))
    finally:
        post_state_msg("stopped")
        print("Closing sensor poller (PIN: " + str(SENSOR_PIN) + ")")

# Start executing the function above
spio_setup()
start_read_cycle()
