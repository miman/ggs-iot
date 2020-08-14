export interface ButtonSensorEvent {
    /** The state of the button (true = button pressed, false = button not pressed) */
    pressed: boolean,
    /** At which GPIO PIN the sensor is connected */
    pin?: string,
    /** The name of this sensor */
    name: string,
    /** The type name of the device */
    type: string,
    /** The name of the device */
    device: string
}
