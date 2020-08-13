import { ServoControllerRequest } from '../dto/servoControllerMsgs'

export class ServoController {
    constructor() {
        console.log("ServoController> Created");
    }

    public setAngle(angle: number, topic: string) {
        let request: ServoControllerRequest = {
            angle: angle
        }
        console.log("ServoController> msg to send on topic [" + topic + "]: " + JSON.stringify(request));
    }
}

export const servoController = new ServoController();
