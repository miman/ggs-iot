import { ButtonSensorEvent } from '../dto/buttonSensorMsgs'

export class ButtonEventHandler {
    constructor() {
        console.log("ButtonEventHandler> Created");
    }

    public handleEvent(event: ButtonSensorEvent, topic: string) {
        console.log("ButtonEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
    }
}

export const buttonEventHandler = new ButtonEventHandler();
