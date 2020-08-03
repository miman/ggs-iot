# distance-poller
Lambda function for Greengrass used to poll a HC-SR04 distance sensor the distance to the object in front of it
The sensor will be polled once every *POLL_INTERVAL* ms and the value will be posted on the MQTT topic **distancepoller/{sensor_name}/value**

## Events
These are the events that i sposted by this long running Lambda service

### Sensor events
Requested sensor value will be returned on topic **distancepoller/{sensor_name}/value**

***The message format***
```
{
    "pins": "Trig_26:Echo_17",
    "distanceMm": 125.1,
    "sensorName": "off-btn",
    "sensorType": "Distance",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **distancepoller/{sensor_name}/started** or **distancepoller/{sensor_name}/stopped**

***The message format***
```
{
    "sensorName": "distance-1",
    "device": "iot-1"
}
```

## Requests
None

## Dynamic settings configurable as environment variables:
DEVICE_NAME: The logical name of the button
TRIG_PIN_NO: The PIN number of the Trig (Output) connector
ECHO_PIN_NO: The PIN number of the Echo (Input) connector
POLL_INTERVAL: The intervall between polls (ms)

# Deployment
This Lambda MUST:
- be run as a long lived Lambda 
- have read rights on the GPIO PINs

You also should define the subscribers that listens to events from this module on these topics
- **distancepoller/+/started** & **distancepoller/+/stopped**
- **distancepoller/+/value**
- OR everything @ **distancepoller/#**

# HW setup - PIN Connection
This block contains information on howto wire the hardware on a Raspberry PI with the default PIN's used in the code

| On device  | On Raspberry PI  |
|---|---|
| GND  | GND  |
| VCC  | 3.3 V  |
| TRIG  | GPIO26  |
| ECHO  | Resistor 560 Ohm -> GPIO07 ->  Resistor 1000 Ohm -> GND |

So ECHO is connected to Resistor 560 Ohm which is connected to GPIO07 which is connected to  Resistor 1000 Ohm which is connected to GND

This is done to lower the voltage from the sensor from 5 V to 3.3 which can be handled by the Raspberry PI (voltage divider).


[Back to Main page](../README.md)
