import { ButtonSensorEvent } from '../dto/buttonSensorMsgs'
import { ruleEngine } from '../ruleEngine'

export class ButtonEventHandler {
    constructor() {
        console.log("ButtonEventHandler> Created");
    }

    public handleEvent(event: ButtonSensorEvent, topic: string) {
        console.log("ButtonEventHandler> msg received on topic [" + topic + "]: " + JSON.stringify(event));
        ruleEngine.handleButtonEvent(event.name, event.pressed);
    }
}

export const buttonEventHandler = new ButtonEventHandler();
