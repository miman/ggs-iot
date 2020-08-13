/*
 * Demonstrates a simple MQTT receiver using Greengrass Core NodeJS SDK
 * This lambda function will receive MQTT msgs and repost the payload on the topic "hello/world"
 */

import ggSdk, { PublishParams } from 'aws-greengrass-core-sdk';
import { distanceEventHandler } from './handlers/distanceEventHandler'
import { buttonEventHandler } from './handlers/buttonEventHandler'
import { lightSensorEventHandler } from './handlers/lightSensorEventHandler'
import { pirMotionSensorEventHandler } from './handlers/pirMotionSensorEventHandler'
import { rfidSensorEventHandler } from './handlers/rfidSensorEventHandler'

const iotClient = new ggSdk.IotData();
const os = require('os');
const util = require('util');

function publishCallback(err: any, data: any) {
    console.log(err);
    console.log(data);
}

let myName = process.env.AWS_IOT_THING_NAME;
const msgToSend: PublishParams = {
    topic: 'echo/output',
    payload: '',
    queueFullPolicy: 'AllOrError',
};

function publishMqttMsg(msg: any, topic: any) {
    let payload = {
        receivedMsg: msg,
        topic: topic,
        deviceName: myName
    };
    msgToSend.payload = JSON.stringify(payload)
    iotClient.publish(msgToSend, publishCallback);
}

// This is a handler which does nothing for this example
exports.handler = function handler(event: any, context: any) {
    console.log("ggs-rule-engine> event received");
    let topic: string = context.clientContext.Custom.subject;
    if (topic.startsWith("distancepoller/")) {
        distanceEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("light_sensor/")) {
        lightSensorEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("btn/")) {
        buttonEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("pir/")) {
        pirMotionSensorEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("rfid/")) {
        rfidSensorEventHandler.handleEvent(event, topic);
    } else {
        console.log("msg received on unknown topic [" + topic + "]: " + event);
    }
    publishMqttMsg(event, context.clientContext.Custom.subject);
};

/*
The received context
{
  invokedFunctionArn: 'arn:aws:lambda:eu-west-1:123456789:function:ggs-mqtt-listen:2',
  awsRequestId: '03048fc4-ead8-40b6-7fbf-6883bcfa11b8',
  functionName: 'ggs-mqtt-listen',
  functionVersion: '2',
  clientContext: { 
    client: {}, 
    Custom: { 
        subject: 'echo/input' 
    }, 
    env: {}
  }
}
*/