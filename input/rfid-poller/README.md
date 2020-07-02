# rfid-poller
Lambda function for Greengrass used to poll a RFID sensor for new TAGs

## Events

### Sensor events
Whenever the sensor reads a new TAG, it will post msg to topic **rfid/read**

***The message format***
```
{
    "id": "783268192",
    "text": "John Smith",
    "sensorName": "id-reader",
    "sensorType": "RFID",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **rfid/started** or **rfid/stopped**

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