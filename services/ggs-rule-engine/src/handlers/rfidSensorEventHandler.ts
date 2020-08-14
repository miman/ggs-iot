import { RfidSensorEvent } from '../dto/rfidSensorMsgs'
import { ruleEngine } from '../ruleEngine'

export class RfidSensorEventHandler {
    constructor() {
        console.log("RfidSensorEventHandler> Created");
    }

    public handleEvent(event: RfidSensorEvent, topic: string) {
        console.log("RfidSensorEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
        ruleEngine.handleRfidEvent(event.name, Number.parseInt(event.id), event.text);
    }
}

export const rfidSensorEventHandler = new RfidSensorEventHandler();
