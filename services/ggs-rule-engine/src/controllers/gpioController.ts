import { mqttSender } from '../util/mqttSender'

export class GpioController {
    constructor() {
        console.log("GpioController> Created");
    }

    /**
     * Send a request to the given topic to set the GPIO PIN on or off
     * @param on    If the GPIO pin is on or off 
     * @param topic The topic to send on
     */
    public setPinState(on: boolean, topic: string) {
        let request = on?"1":"0";
        mqttSender.publishMqttMsg(request, topic);
        console.log("GpioController> msg to send on topic [" + topic + "]: " + JSON.stringify(request));
    }
}

export const gpioController = new GpioController();
