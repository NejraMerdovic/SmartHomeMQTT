# SmartHomeMQTT
Developed skill for Amazon Alexa Assistant

Skill for Amazon Alexa Assistent was created using Alexa Skills Kit (ASK). Skill invocation 
name and all intent launch phrases are defined there. When the user gives a task to the 
Amazon Alexa assistant with a voice or text command, the given code of the Lambda function 
(lamda_function.py) is run in the background. Through the program code, the user's request 
is processed and connected to the Mosquitto broker. The broker sends the user's message 
to all clients who have subscribed to the corresponding topic. Through MQTTLens, all 
existing topics are defined and incoming messages can be read there. Through the Thonny 
development environment, code was created in MicroPython for the configuration of the 
used wi-fi network and the mqtt protocol, as well as the main code in which the device 
is subscribed to all defined topics, and the task based on the read message is done
(turning on/off the LED diode, changing the intensity of the color of the LED diode, 
changing the color of the RBG diode to the desired, etc.).
