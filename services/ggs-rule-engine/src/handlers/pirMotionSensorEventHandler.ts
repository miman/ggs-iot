import { PirMotionSensorEvent } from '../dto/pirMotionSensorMsgs'
import { ruleEngine } from '../ruleEngine'

export class PirMotionSensorEventHandler {
    constructor() {
        console.log("PirMotionSensorEventHandler> Created");
    }

    public handleEvent(event: PirMotionSensorEvent, topic: string) {
        console.log("PirMotionSensorEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
        ruleEngine.handlePirMotionSensorEvent(event.name);
    }
}

export const pirMotionSensorEventHandler = new PirMotionSensorEventHandler();
