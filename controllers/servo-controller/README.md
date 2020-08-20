# servo-controller
Contains an input lambda controlling a servo relay

This lambda function will control the relay based on input on the topic **servo/+/set**

If we get a msg on topic **servo/+/set** we will activate the power

We assume the Servo relay is on PIN GPIO4

## Events

### Sensor events
Whenever the power controller activates or deactivates the servo relay it will send an event on **servo/{thing-name}/on** or **servo/{thing-name}/off**

state can be on or off

When the servo is moved an event is sent on MQTT topic **servo/{thing-name}/moved**

***The message format***
```
{
    "deviceName": "id-reader",
    "device": "iot-1"
    "state": "on",
    "type": "servo"
}
```

## Dynamic settings configurable as environment variables:
DEVICE_NAME: The logical name of the sensor
IO_PIN_NO: The PIN the Servo relay uses

# HW setup - PIN Connection
This block contains information on howto wire the hardware on a Raspberry PI with the default PIN's used in the code

| On device  | On Raspberry PI  |
|---|---|
| GND  | GND  |
| VCC  | 5 V  |
| Signal  | GPIO04 |

[Back to Main page](../README.md)
