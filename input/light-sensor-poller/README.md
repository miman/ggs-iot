# light-sensor-poller
Lambda function for Greengrass used to poll a light sensor for how bright it is
For each new (non-same) value it will send an event on topic **light_sensor/value**

## Events

### Sensor events
For each new (non-same) value it will send an event on topic **light_sensor/value**

***The message format***
```
{
    "pin": 12,
    "state": "on",
    "sensorName": "light-sensor-1",
    "sensorType": "LIGHT_SENSOR",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **light_sensor/started** or **light_sensor/stopped**

***The message format***
```
{
    "sensorName": "light-sensor-1",
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
| LEG-1  | GPIO06 -> (+) 1 micro-Farad capacitor (-) -> GND |
| LEG-2  | 3.3 V  |

[Back to Main page](../README.md)
