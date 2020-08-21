# power-controller
Contains an input lambda controlling a power relay & a test LED

This lambda function will control the relay (on/off) based on input on the topic **pwrRelay/+/set**

We assume the Power relay is on PIN GPIO12
We assume the LED is on PIN GPIO13

## Events

### Sensor events
Whenever the power controller activates or deactivates the power relay it will send an event on **pwrRelay/on** or **pwrRelay/off**

state can be on or off

***The message format***
```
{
    "deviceName": "id-reader",
    "device": "iot-1"
    "state": "on"
}
```

## Dynamic settings configurable as environment variables:
DEVICE_NAME: The logical name of the sensor
IO_PIN_NO: The PIN the Power relay uses
LED_IO_PIN_NO: The PIN the LED uses

# HW setup - PIN Connection
This block contains information on howto wire the hardware on a Raspberry PI with the default PIN's used in the code

| On device  | On Raspberry PI  |
|---|---|
| GND  | GND  |
| VCC  | 5 V  |
| IN1  | TBD  |
| IN2  | TBD |

[Back to Main page](../README.md)