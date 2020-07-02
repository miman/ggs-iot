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

# PIN Connection

RC522   --  R-PI
=================
3.3     --  3.3

RST     --  PIN 22 / GPIO23

GND     --  GND

MISO    --  PIN 21 (MISO) / SPMISO / GPIO09

MOSI    --  PIN 19 (MOSI) / SPMOSI / GPIO10

SCK     --  PIN 23 (SCK) / SPISCLK/ GPIO11                        SCK = Selektor

SDA     --  PIN 24 (SDA) / SPICEO / GPIO08

[Back to Main page](../README.md)