from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()  # create skill builder object

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):  # The can_hande metod returns a Boolean value indicating
        # if the request handler can create an appropriate response for the request
        # type: #(HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)  # The can_handle function returns True if the incoming request is a LaunchRequest

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to your custom alexa application!"
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response  # The handle function generates and returns a basic greeting response

import paho.mqtt.client as mqtt
import time

class SwitchDeviceOnOffIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SwitchDeviceOnOffIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        device = get_slot_value(handler_input=handler_input, slot_name="device")
        state =  get_slot_value(handler_input=handler_input, slot_name="state")

        broker = "test.mosquitto.org"
        client = mqtt.Client("python1")
        client.connect(broker)
        client.subscribe("testetf/" + str(device))
        client.publish("testetf/"+str(device), state)
        client.disconnect()

        speech_text = str(device)+" is switched "+str(state)
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Message1", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class SetColorIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SetColorIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        color = get_slot_value(handler_input=handler_input, slot_name="color")

        broker = "test.mosquitto.org"
        client = mqtt.Client("python1")
        client.connect(broker)
        client.subscribe("testetf/rgb")
        client.publish("testetf/rgb", color)
        client.disconnect()

        speech_text = "You chose "+str(color)+". Now you can choose another color"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Message2", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class PWMIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PWMIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        number = get_slot_value(handler_input=handler_input, slot_name="number")
        device = get_slot_value(handler_input=handler_input, slot_name="device")

        broker = "test.mosquitto.org"
        client = mqtt.Client("python1")
        client.connect(broker)
        client.subscribe("testetf/"+ str(device))
        client.publish("testetf/"+ str(device), int(number))
        client.disconnect()

        speech_text = str(device)+" is turned on to "+str(number)+" percent"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Message3", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can ask me to switch smart device on or off. Also you can ask me to set color of diode to the desired one or to adjust the intensity of some smart device."

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
            handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response

from ask_sdk_core.dispatch_components import AbstractExceptionHandler

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())  # Creating the Lambda handler
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(SetColorIntentHandler())
sb.add_request_handler(PWMIntentHandler())
sb.add_request_handler(SwitchDeviceOnOffIntentHandler())

sb.add_exception_handler(AllExceptionHandler())

lambda_handler = sb.lambda_handler()
