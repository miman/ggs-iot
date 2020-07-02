# btn-poller
Lambda function for Greengrass used to poll a Button for state changes

## Events

### Sensor events
If the sensor is active/inactive, it will post msg to topic **btn/on** or **btn/off**

***The message format***
```
{
    "pin": 12,
    "state": "on",
    "sensorName": "off-btn",
    "sensorType": "Button",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **btn/started** or **btn/stopped**

***The message format***
```
{
    "sensorName": "off-btn",
    "device": "iot-1"
}
```


## Dynamic settings configurable as environment variables:
IO_PIN_NO: The PIN the sensor uses
DEVICE_NAME: The logical name of the sensor


[Back to Main page](../README.md)