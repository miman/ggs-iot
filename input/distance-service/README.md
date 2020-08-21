# distance-service
Lambda function for Greengrass which enables a client to request for distance sensor data or set a trigger for the data.

This is done in a separate Lambda from the distance-poller Lambda while the actual poller Lambda is a long running Lambda it cannot listen to incoming MQTT msgs.

So this Lambda can listen to requests from the clients and also events from the actual poller, it caches and then resends the events when requested by the client.

## Limitations
For now it can only handle one distance poller sensor

## Requests

### Distance value request
Requests are listened to on MQTT topic **distance/{sensor_name}/request**

***The message format***
OBS !, Only one-time works for now.

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
    "name": "off-btn",
    "type": "DISTANCE_SENSOR",
    "device": "iot-1"
}
```


## Dynamic settings configurable as environment variables:
none

[Back to Main page](../README.md)