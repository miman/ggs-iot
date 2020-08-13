export interface RfidSensorEvent {
    /** The text contained in the RFID tag */
    text: string,
    /** The Id number of the RFID tag */
    id: string,
    /** The name of this sensor */
    name: string,
    /** The type name of the device */
    type: string,
    /** The name of the device */
    device: string
}
