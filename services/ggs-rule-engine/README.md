# ggs-rule-engine
Lambda function for Greengrass listening to events from sensors and executing the rules sent to it using a dynamic rule engine

## Prerequisites

### Resources
No resources needs to be created for this project

### Subscriptions
You MUST add a subscription for the following topics with this Lambda as **Target** & the different sensor Lambdas as **Source**
- distancepoller/#
- light_sensor/#
- btn/#
- pir/#
- rfid/#

You MUST add a subscription for the following topics with this Lambda as **Source** & the different sensor Lambdas as **Target**
- servo/#
- pwrRelay/#

## Usage
You build the project runnin the **npm run-script build** command, this will compile the Typescript files to Javascript
You create a deployment package by running the **npm run-script package** which creates a zip file that can be uploaded to the Lambda function

OBS.
When the Lambda has been uploaded you MUST do the following 2 steps before you can deploy theLambda to a Greengrass device
1. Create a version
2. Create an Alias

The alias should then be choosen when creating/updating the Lambda in the Greegrass group before deploying it.

Remember that the Subscriptions MUST be updated with the new version for the Lambda to work !!

[Back to Main page](../README.md)
