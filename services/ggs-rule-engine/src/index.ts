/*
 * The main handler function
 */

import { distanceEventHandler } from './handlers/distanceEventHandler'
import { buttonEventHandler } from './handlers/buttonEventHandler'
import { lightSensorEventHandler } from './handlers/lightSensorEventHandler'
import { pirMotionSensorEventHandler } from './handlers/pirMotionSensorEventHandler'
import { rfidSensorEventHandler } from './handlers/rfidSensorEventHandler'

let myName: string = process.env.AWS_IOT_THING_NAME || "unknown";

// This is a handler which does nothing for this example
exports.handler = function handler(event: any, context: any) {
    // console.log("ggs-rule-engine> event received");
    let topic: string = context.clientContext.Custom.subject;
    if (topic.startsWith("distancepoller/") && topic.includes("/value")) {
        distanceEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("light_sensor/") && topic.includes("/value")) {
        lightSensorEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("btn/") && (topic.includes("/on") || topic.includes("/off"))) {
        buttonEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("pir/") && topic.includes("/value")) {
        pirMotionSensorEventHandler.handleEvent(event, topic);
    } else if (topic.startsWith("rfid/") && topic.includes("/read")) {
        rfidSensorEventHandler.handleEvent(event, topic);
    } else {
        console.log("msg received on unknown topic [" + topic + "]: " + event);
    }
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