# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
import sys
sys.path.append('/home/hoangnam/Documents/code/xProjects/bkchatbot')
# from backend.logic.schedule4day import get_response_msg
from backend.logic.schedule_duclking import get_respone

class ActionShowSchedule(Action):

    def name(self) -> Text:
        return "action_show_schedule"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        sender_id = tracker.sender_id
        message = tracker.latest_message.get('text')
        # response = get_response_msg(sender_id, message)
        response = get_respone(sender_id, message, entities)
        dispatcher.utter_message(text=response)
        return []