# ggs-iot
This project contains a number of Greengrass IoT Lambdas accessing physical hardware and communicating over AWS IoT / MQTT, so communicating with a backend is very simple as well as communicating with other Lambdas in the Greegrass device..

By using these Lambdas you can focus your implementation on working with MQTT interfaces accessing hardware instead of the GPIO detailed code :-)

There are both input & output devices, example of devices that can be communicated with are:
* Input
  * Button
  * NFC Reader
  * Depth sensor
  * PIR/Motion sensor
  * Light sensor
* Output/Controllers
  * Relay controlling 220/110V
  * Servo motor
  * LED

# Folder structure
This section describes the folder structure of this project

## Controllers
The [controllers](./controllers/README.md) folder contains controller lambdas, which control HW units

## Input
The [input](./input/README.md) folder contains input lambdas reading input data from HW units

## Zip-bat files
These are used to zip the project into a zip file that can be uploaded as a Lambda to AWS

# Webcasts
If you are new to working with AWS IoT Greengrass, check the project linked below for example Lambdas and a link to a webcast series on what AWS configurations that are needed. 

[rpi-greengrass](https://github.com/miman/rpi-greengrass)
