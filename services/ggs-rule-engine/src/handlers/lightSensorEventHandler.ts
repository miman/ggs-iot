import { LightSensorEvent } from '../dto/lightSensorMsgs'

export class LightSensorEventHandler {
    constructor() {
        console.log("LightSensorEventHandler> Created");
    }

    public handleEvent(event: LightSensorEvent, topic: string) {
        console.log("LightSensorEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
    }
}

export const lightSensorEventHandler = new LightSensorEventHandler();
