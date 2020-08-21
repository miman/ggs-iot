# btn-poller
Lambda function for Greengrass used to poll a Button for state changes

## Events

### Sensor events
If the sensor is active/inactive, it will post msg to topic **btn/{sensor-name}/on** or **btn/{sensor-name}/off**

***The message format***
```
{
    "pin": 12,
    "pressed": true,
    "name": "off-btn",
    "type": "BUTTON",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **btn/{sensor-name}/started** or **btn/{sensor-name}/stopped**

***The message format***
```
{
    "name": "off-btn",
    "type": "BUTTON",
    "device": "iot-1"
}
```

## Dynamic settings configurable as environment variables:
IO_PIN_NO: The PIN the sensor uses
DEVICE_NAME: The logical name of the sensor

# HW setup - PIN Connection
This block contains information on howto wire the hardware on a Raspberry PI with the default PIN's used in the code

| On device  | On Raspberry PI  |
|---|---|
| leg 1  | GND  |
| leg 2  | GPIO19  |

[Back to Main page](../README.md)