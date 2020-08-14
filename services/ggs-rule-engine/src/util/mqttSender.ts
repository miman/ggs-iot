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
        let publishParams: PublishParams = {
            topic: topic,
            payload: JSON.stringify(msg),
            queueFullPolicy: 'AllOrError',
        };
        this.iotClient.publish(publishParams, this.publishCallback);
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
