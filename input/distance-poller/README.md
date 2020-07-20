# btn-poller
Lambda function for Greengrass used to poll a HC-SR04 distance sensor the distance to the object in front of it

## Requests

### Distance value request
Requests are listened to on MQTT topic **distance/{sensor_name}/request**

***The message format***
One-time is used if we want the last known distance directly & once
```
{
    "type": "one-time"
}
```
Or
Timer is used if we want the distance value event at a regular interval
```
{
    "type": "timer",
    "intervalMs": 1000
}
```
Or
This example trigger will make the sensor to send any value that is more than 2500 mm or less than 100 mm
once = true -> it will then not resend this until the value has regained normal state (true)
once = false -> all values outside this span (false)
```
{
    "type": "trigger",
    "lessThanMm": 100,
    "moreThanMm": 2500,
    "once": true
}
```


## Events

### Sensor events
Requested sensor value will be returned on topic **distance/{sensor_name}/value**

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
When this poller is started/stopped it will post a msg to topic **distance/started** or **distance/stopped**

***The message format***
```
{
    "sensorName": "distance-1",
    "device": "iot-1"
}
```


## Dynamic settings configurable as environment variables:
DEVICE_NAME: The logical name of the button
TRIG_PIN_NO: The PIN number of the Trig (Output) connector
ECHO_PIN_NO: The PIN number of the Echo (Input) connector
POLL_INTERVAL: The intervall between polls (ms)

[Back to Main page](../README.md)