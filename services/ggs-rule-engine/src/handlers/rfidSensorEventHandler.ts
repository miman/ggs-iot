import { RfidSensorEvent } from '../dto/rfidSensorMsgs'

export class RfidSensorEventHandler {
    constructor() {
        console.log("RfidSensorEventHandler> Created");
    }

    public handleEvent(event: RfidSensorEvent, topic: string) {
        console.log("RfidSensorEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
    }
}

export const rfidSensorEventHandler = new RfidSensorEventHandler();
