import { LightSensorEvent } from '../dto/lightSensorMsgs'
import { ruleEngine } from '../ruleEngine'

export class LightSensorEventHandler {
    constructor() {
        console.log("LightSensorEventHandler> Created");
    }

    public handleEvent(event: LightSensorEvent, topic: string) {
        console.log("LightSensorEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
        ruleEngine.handleLightSensorEvent(event.name, event.value);
    }
}

export const lightSensorEventHandler = new LightSensorEventHandler();
