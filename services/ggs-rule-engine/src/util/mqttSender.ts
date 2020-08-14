import ggSdk, { PublishParams, IotData } from 'aws-greengrass-core-sdk';

/**
 * This class is used tyo post message onto the AWS IoT MQTT server
 */
export class MqttSender {
    iotClient: IotData;

    constructor() {
        this.iotClient = new ggSdk.IotData();

        this.publishMqttMsg = this.publishMqttMsg.bind(this);
        this.publishCallback = this.publishCallback.bind(this);
    }

    /**
     * Send the given message on the given topic on the AWS MQTT srv
     * @param msg The message to send
     * @param topic The topic name to send on
     */
    public publishMqttMsg(msg: any, topic: string) {
        let payload: string = JSON.stringify(msg);
        console.log("MqttSender> sending msg to topic [" + topic + "]: " + payload);
        let publishParams: PublishParams = {
            topic: topic,
            payload: payload,
            queueFullPolicy: 'AllOrError',
        };
        try {
            this.iotClient.publish(publishParams, this.publishCallback);
        } catch (err) {
            console.log("MqttSender> publishMqttMsg failed: " + JSON.stringify(err))
        }
    }

    private publishCallback(err: any, data: any) {
        if (err) {
            console.log("MqttSender> send error: " + err);
        }
        if (data) {
            console.log("MqttSender> send response: " + data);
        }
    }
}

export const mqttSender = new MqttSender();
