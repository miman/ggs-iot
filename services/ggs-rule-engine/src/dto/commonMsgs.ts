export enum ACTVATION_STATE {
    STARTED = "started",
    STOPPED = "stopped"
}

/**
 * This start/stop event is sent whenever a poller service is started/stopped
 */
export interface DeviceStartedEvent {
    /** The name of this sensor */
    name: string,
    /** The type name of the device */
    type: string,
    /** The name of the device */
    device: string,
    /** The state of the sensor */
    state?: ACTVATION_STATE,
    /** At which GPIO PIN the sensor is connected */
    pin?: string
}
