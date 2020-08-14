export interface PirMotionSensorEvent {
    /** The state of the PIR motion sensor (true = movement noticed, false = no movement noticed) */
    presence: boolean,
    /** At which GPIO PIN the sensor is connected */
    pin?: string,
    /** The name of this sensor */
    name: string,
    /** The type name of the device */
    type: string,
    /** The name of the device */
    device: string
}
