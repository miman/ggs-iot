import { DistanceSensorEvent } from '../dto/distanceMsgs'

export class DistanceEventHandler {
    constructor() {
        console.log("DistanceEventHandler> Created");
    }

    public handleEvent(event: DistanceSensorEvent, topic: string) {
        console.log("DistanceEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
    }
}

export const distanceEventHandler = new DistanceEventHandler();
