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
    "name": "id-reader",
    "type": "RFID_READER",
    "device": "iot-1"
}
```

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **rfid/started** or **rfid/stopped**

***The message format***
```
{
    "sensorName": "door-sensor",
    "type": "RFID_READER",
    "device": "iot-1"
}
```


## Dynamic settings configurable as environment variables:
IO_PIN_NO: The PIN the sensor uses
DEVICE_NAME: The logical name of the sensor

# HW setup - PIN Connection
This block contains information on howto wire the hardware on a Raspberry PI with the default PIN's used in the code

| On device (RC522) | On Raspberry PI  |
|---|---|
| GND  | GND  |
| 3.3  | 3.3  |
| RST  | PIN 22 / GPIO23  |
| MISO  | PIN 19 (MOSI) / SPMOSI / GPIO10  |
| MOSI  | PIN 19 (MOSI) / SPMOSI / GPIO10  |
| SCK  | PIN 23 (SCK) / SPISCLK/ GPIO11 |
| SDA  | PIN 24 (SDA) / SPICEO / GPIO08 |

SCK = Selektor

[Back to Main page](../README.md)