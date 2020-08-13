import { Engine } from 'json-rules-engine'
import { servoController } from './controllers/servoController'

/**
 * This is a dynamic rule engine
 */
export class RuleEngine {
    engine: Engine;
    /**
     * Define facts the engine will use to evaluate the conditions above.
     * Facts may also be loaded asynchronously at runtime; see the advanced example below
     */
    facts: any = {};

    constructor() {
        this.engine = new Engine()

        this.facts = {
            btnPresses: 0,
            rfidReads: 0,
            lightSensorReadings: 0,
            pirMotionSensorReadings: 0,
            distanceSensorReadings: 0
        }

        this.addRules();
    }

    private addRules() {
        // define a rule for detecting the player has exceeded foul limits.
        this.engine.addRule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'btnPresses',
                        operator: 'greaterThanInclusive',
                        value: 4
                    }]
                }, {
                    all: [{
                        fact: 'lightSensorReadings',
                        operator: 'equal',
                        value: 4
                    }, {
                        fact: 'rfidReads',
                        operator: 'greaterThanInclusive',
                        value: 1
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truthy
                type: 'lightsOn',
                params: {
                    message: 'We should turn the lights on'
                }
            }
        });

        this.engine.addRule({
            conditions: {
                any: [{
                    all: [{
                        fact: 'pirMotionSensorReadings',
                        operator: 'greaterThanInclusive',
                        value: 2
                    }]
                }]
            },
            event: {  // define the event to fire when the conditions evaluate truthy
                type: 'TurnOnRelay',
                params: {
                    message: 'Turn on relay',
                    topic: "servo/123/set",
                    angle: this.facts.btnPresses
                }
            }
        });
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
                    if (event.type.match("TurnOnRelay") && event.params) {
                        servoController.setAngle(event.params.angle, event.params.topic);
                    }
                })
            })
    }

    public handleButtonEvent(name: string) {
        this.facts.btnPresses += 1;
        this.runEngine();
    }

    public handlePirMotionSensorEvent(name: string) {
        this.facts.pirMotionSensorReadings += 1;
        this.runEngine();
    }
}

export let ruleEngine = new RuleEngine();
