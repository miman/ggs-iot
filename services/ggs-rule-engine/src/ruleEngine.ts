import { Engine, Rule } from 'json-rules-engine';
import { servoController } from './controllers/servoController';
import { gpioController } from './controllers/gpioController';

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
            distanceSensorProcessed: true
        }

        this.addRules();
    }

    private addRules() {
        let rule: any = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'btnPressed',
                        operator: 'equal',
                        value: 'true'
                    },{
                        fact: 'lastButtonPressedState',
                        operator: 'equal',
                        value: 'false'
                    },{
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
                type: 'TurnServo',
                params: {
                    message: 'Reset Servo',
                    topic: "servo/servo-1/set",
                    angle: 0
                }
            }
        });

        let ruleStr: string = rule.toJSON();
        console.log("Rule 1: " + ruleStr);
        // define a rule for detecting if we should turn the relay off based on :
        // - the button was pressed when the relay is active
        // - the off relay card was used
        this.engine.addRule(rule);

        // define a rule for detecting if we should turn the relay on based on :
        // - any RFID card was used
        rule = new Rule({
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
                type: 'TurnServo',
                params: {
                    message: 'Turn on relay',
                    topic: "servo/servo-1/set",
                    angle: 90
                }
            }
        });
        this.engine.addRule(rule);

        // define a rule for detecting if we should turn the LED on based on :
        // - If the button is pressed
        rule = new Rule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'btnPressed',
                        operator: 'equal',
                        value: 'true'
                    },{
                        fact: 'lastButtonPressedState',
                        operator: 'equal',
                        value: 'false'
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truth
                type: 'SetGpioPin',
                params: {
                    message: 'Activate GPIO PIN',
                    topic: "gpio/" + this.deviceName + "/27/write",
                    value: true
                }
            }
        });
        this.engine.addRule(rule);
        rule = new Rule({
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
                type: 'SetGpioPin',
                params: {
                    message: 'Activate GPIO PIN',
                    topic: "gpio/" + this.deviceName + "/27/write",
                    value: false
                }
            }
        });
        this.engine.addRule(rule);
    }

    public runEngine() {
        // Run the engine to evaluate
        this.engine
            .run(this.facts)
            .then(results => {
                // 'results' is an object containing successful events, and an Almanac instance containing facts
                results.events.forEach(event => {
                    if (event.params) {
                        console.log("RuleEngine> " + event.params.message)
                    } else {
                        console.log("RuleEngine> No message in event")
                    }
                    if (event.type.match("TurnServo") && event.params) {
                        servoController.setAngle(event.params.angle, event.params.topic);
                    }
                    if (event.type.match("SetGpioPin") && event.params) {
                        gpioController.setPinState(event.params.value, event.params.topic)
                    }
                })
            })
    }

    public handleButtonEvent(name: string, pressed: boolean) {
        this.facts.btnPresses += 1;
        this.facts.btnPressed = pressed;
        this.runEngine();
        this.facts.lastButtonPressedState = pressed;
    }

    public handlePirMotionSensorEvent(name: string) {
        this.facts.pirMotionSensorReadings += 1;
        this.runEngine();
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
