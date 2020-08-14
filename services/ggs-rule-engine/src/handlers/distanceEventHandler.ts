import { DistanceSensorEvent } from '../dto/distanceMsgs'
import { ruleEngine } from '../ruleEngine'

export class DistanceEventHandler {
    constructor() {
        console.log("DistanceEventHandler> Created");
    }

    public handleEvent(event: DistanceSensorEvent, topic: string) {
        console.log("DistanceEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
        ruleEngine.handleDistanceEvent(event.name, event.distanceMm);
    }
}

export const distanceEventHandler = new DistanceEventHandler();
