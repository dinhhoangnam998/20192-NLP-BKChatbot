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
sys.path.append(r'C:\Users\HoangNam\Documents\Code\xProject\20192-NLP-BTL-BKChatbot')
from backend.logic.schedule_by_time import schedule_by_time
from backend.logic.schedule_by_subject import schedule_by_subject

class ActionShowScheduleByTime(Action):

    def name(self) -> Text:
        return "action_show_schedule"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        sender_id = tracker.sender_id
        # message = tracker.latest_message.get('text')
        response = schedule_by_time.get_response(sender_id, entities)
        dispatcher.utter_message(text=response)
        return []


class ActionShowScheduleBySubject(Action):

    def name(self) -> Text:
        return "action_show_subject_information"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # entities = tracker.latest_message['entities']
        sender_id = tracker.sender_id
        message = tracker.latest_message.get('text')
        response = schedule_by_subject.get_response(sender_id, message)
        dispatcher.utter_message(text=response)
        return []