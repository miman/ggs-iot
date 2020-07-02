# pir-poller
Lambda function for Greengrass used to poll a PIR (motion sensor) for state changes
If motion is detected it will send an on-event
When no motion is detected any longer, an off-event is sent

## Events

### Sensor events
If the sensor is active/inactive, it will post msg to topic **pir/on** or **pir/off**

***The message format***
```
{
    "pin": 12,
    "state": "on",
    "sensorName": "door-sensor",
    "sensorType": "PIR",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **pir/started** or **pir/stopped**

***The message format***
```
{
    "sensorName": "door-sensor",
    "device": "iot-1"
}
```


## Dynamic settings configurable as environment variables:
IO_PIN_NO: The PIN the sensor uses
DEVICE_NAME: The logical name of the sensor


[Back to Main page](../README.md)