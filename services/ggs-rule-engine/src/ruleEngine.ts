import { Engine, Rule } from 'json-rules-engine';
import { servoController } from './controllers/servoController';
import { gpioController } from './controllers/gpioController';
import { mqttSender } from './util/mqttSender'

enum RULE_EVENTS {
    TurnServo = "TurnServo",
    SetGpioPin = "SetGpioPin",
    SendEvent = "SendEvent"
}

/**
 * This is a dynamic rule engine
 */
export class RuleEngine {
    engine: Engine;
    deviceName: string;
    /**
     * Define facts the engine will use to evaluate the conditions above.
     * Facts may also be loaded asynchronously at runtime; see the advanced example below
     */
    facts: any = {};

    constructor() {
        this.engine = new Engine()
        this.deviceName = process.env.AWS_IOT_THING_NAME || "?";

        this.facts = {
            btnPresses: 0,
            rfidReads: 0,
            lightSensorReadings: 0,
            pirMotionSensorReadings: 0,
            distanceSensorReadings: 0,
            btnPressed: false,
            lastButtonPressedState: false,
            lastLightSensorValue: 0,
            lastPirState: false,
            relayActive: false,
            rfidCardNo: 0,
            rfidProcessed: true,
            lightSensorValue: 0,
            lightSensorProcessed: true,
            distanceSensorValue: 0,
            distanceSensorProcessed: true,
            pirMotionPresence: false,
            lastPirMotionPresenceState: true
        }

        this.addRules();
    }

    private addRules() {
        let rule1: any = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'btnPressed',
                        operator: 'equal',
                        value: 'true'
                    }, {
                        fact: 'relayActive',
                        operator: 'equal',
                        value: true
                    }]
                }, {
                    all: [{
                        fact: 'rfidCardNo',
                        operator: 'equal',
                        value: 291909929871
                    }, {
                        fact: 'rfidProcessed',
                        operator: 'equal',
                        value: false
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truthy
                type: RULE_EVENTS.TurnServo.toString(),
                params: {
                    message: 'Reset Servo',
                    topic: "servo/servo-1/set",
                    angle: 0
                }
            }
        });

        // define a rule for detecting if we should turn the relay off based on :
        // - the button was pressed when the relay is active
        // - the off relay card was used
        this.engine.addRule(rule1);

        // define a rule for detecting if we should turn the relay on based on :
        // - any RFID card was used
        let rule2: any = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'rfidCardNo',
                        operator: 'equal',
                        value: 1071914926771
                    }, {
                        fact: 'rfidProcessed',
                        operator: 'equal',
                        value: false
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truthy
                type: RULE_EVENTS.TurnServo.toString(),
                params: {
                    message: 'Turn on relay',
                    topic: "servo/servo-1/set",
                    angle: 90
                }
            }
        });
        this.engine.addRule(rule2);

        // define a rule for detecting if we should turn the LED on based on :
        // - If the button is pressed
        let rule3: any = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'btnPressed',
                        operator: 'equal',
                        value: 'true'
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truth
                type: RULE_EVENTS.SetGpioPin.toString(),
                params: {
                    message: 'Activate GPIO PIN',
                    topic: "gpio/" + this.deviceName + "/27/write",
                    value: true
                }
            }
        });
        this.engine.addRule(rule3);
        let rule4: any = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'btnPressed',
                        operator: 'equal',
                        value: 'false'
                    },{
                        fact: 'lastButtonPressedState',
                        operator: 'equal',
                        value: 'true'
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truth
                type: RULE_EVENTS.SetGpioPin.toString(),
                params: {
                    message: 'Deactivate GPIO PIN',
                    topic: "gpio/" + this.deviceName + "/27/write",
                    value: false
                }
            }
        });

        this.engine.addRule(rule4);

        let rule5: any = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'lightSensorValue',
                        operator: 'lessThanInclusive',
                        value: 40
                    }, {
                        fact: 'lightSensorProcessed',
                        operator: 'equal',
                        value: 'false'
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truth
                type: RULE_EVENTS.SendEvent.toString(),
                params: {
                    message: 'Deactivate GPIO PIN',
                    topic: "light/" + this.deviceName + "/state",
                    payload: {
                        msg: "The light is below 40",
                        value: this.facts.lightSensorValue
                    }
                }
            }
        });
        let ruleStr: string = rule5.toJSON();
        console.log(">>> RuleEngine> Rule: " + ruleStr);

        this.engine.addRule(rule5);
    }

    public runEngine() {
        // Run the engine to evaluate
        this.engine
            .run(this.facts)
            .then(results => {
                // 'results' is an object containing successful events, and an Almanac instance containing facts
                results.events.forEach(event => {
                    console.log("RuleEngine> Rule triggered: " + event.type)
                    if (event.params) {
                        console.log("RuleEngine> Rule message: " + event.params.message)
                        switch (event.type) {
                            case "TurnServo":
                                servoController.setAngle(event.params.angle, event.params.topic);
                                break;
                            case "SetGpioPin":
                                gpioController.setPinState(event.params.value, event.params.topic)
                                break;
                            case "SendEvent":
                                mqttSender.publishMqttMsg(event.params.payload, event.params.topic);
                                break;
                            default:
                                break;
                        }
                    }
                })
            })
    }

    public handleButtonEvent(name: string, pressed: boolean) {
        this.facts.btnPresses += 1;
        this.facts.btnPressed = pressed;
        console.log("facts before: " + JSON.stringify(this.facts));
        this.runEngine();
        this.facts.lastButtonPressedState = pressed;
        console.log("facts after: " + JSON.stringify(this.facts));
    }

    public handlePirMotionSensorEvent(name: string, presence: boolean) {
        this.facts.pirMotionSensorReadings += 1;
        this.facts.pirMotionPresence = presence;
        this.runEngine();
        this.facts.lastPirMotionPresenceState = presence;
    }

    public handleRfidEvent(name: string, id: number, text: string) {
        this.facts.rfidReads += 1;
        this.facts.rfidCardNo = id;
        this.facts.rfidCardText = text;
        this.facts.rfidProcessed = false;
        this.runEngine();
        this.facts.rfidProcessed = true;
    }

    public handleLightSensorEvent(name: string, value: number) {
        this.facts.lightSensorReadings += 1;
        this.facts.lightSensorValue = value;
        this.facts.lightSensorProcessed = false;
        this.runEngine();
        this.facts.lightSensorProcessed = true;
    }

    public handleDistanceEvent(name: string, distanceMm: number) {
        this.facts.distanceSensorReadings += 1;
        this.facts.distanceSensorValue = distanceMm;
        this.facts.distanceSensorProcessed = false;
        this.runEngine();
        this.facts.distanceSensorProcessed = true;
    }
}

export let ruleEngine = new RuleEngine();
