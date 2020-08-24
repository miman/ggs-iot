# water-sensor-poller
Lambda function for Greengrass used to poll a water moisture sensor for how much water it senses.
For each new (non-same) value it will send an event on topic **water_sensor/value**
The analog value is sent through a MCP3008 ADC converter to get the digital value

## Events

### Sensor events
For each new (non-same) value it will send an event on topic **water_sensor/value**

***The message format***
```
{
    "pin": 12,
    "value": 43200,
    "waterDetected": true
    "name": "water-sensor-1",
    "type": "WATER_SENSOR",
    "device": "iot-1"
}
```

In my test the values ranged between 28000 - 65472

The level when the board indicates that water was detected is set using the potentiometer on the water sensor board.

### Lambda lifecycle events
When this poller is started/stopped it will post a msg to topic **water_sensor/started** or **water_sensor/stopped**

***The message format***
```
{
    "name": "water-sensor-1",
    "type": "WATER_SENSOR",
    "state": "started",
    "pin": "5",
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
| VCC  | 3.3 V  |
| GND  | Ground  |
| D0  | GPIO22 |
| A0  | Channel 0 on a MCP3008 ADC  |

MCP3008 ADC setup
-----------------
| MCP3008  | On Raspberry PI  |
|---|---|
| VDD  | 3.3 V  |
| VREF  | 3.3 V  |
| AGND  | Ground  |
| CLK  | SPSCLK |
| DOUT  | SPIMISO  |
| DIN  | SPIMOSI  |
| CS  | GPIO5  |
| DGND  | Ground  |
| C0  | A0 on Water sensor  |


[Back to Main page](../README.md)
