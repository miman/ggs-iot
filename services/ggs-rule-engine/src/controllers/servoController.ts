import { ServoControllerRequest } from '../dto/servoControllerMsgs'
import { mqttSender } from '../util/mqttSender'

export class ServoController {
    constructor() {
        console.log("ServoController> Created");
    }

    /**
     * Send a request to the given topic to set the servo angle to the given value
     * @param angle 
     * @param topic 
     */
    public setAngle(angle: number, topic: string) {
        let request: ServoControllerRequest = {
            angle: angle
        }
        mqttSender.publishMqttMsg(request, topic);
        console.log("ServoController> msg to send on topic [" + topic + "]: " + JSON.stringify(request));
    }
}

export const servoController = new ServoController();
