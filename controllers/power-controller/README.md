# power-controller
Contains an input lambda controlling a power relay & a test LED

This lambda function will control the relay based on input on the topic **rfid/+/read** & **btn/+/state**

If we get a msg on topic **rfid/+/read** we will activate the power
If we get a msg on topic **btn/+/on** we will de-activate the power

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

[Back to Main page](../README.md)