# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

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
from backend.logic.schedule_by_time import schedule_by_time
from backend.logic.schedule_by_subject import schedule_by_subject
from backend.db import db

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

class ActionAskSidIfNeed(Action):

    def name(self) -> Text:
        return "action_ask_sid_if_need"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender_id = tracker.sender_id
        if not db.has_sid(sender_id):
            dispatcher.utter_message(text='Mà, mã số sinh viên của bạn là gì ấy nhỉ!?')
        return []


class ActionSaveSid(Action):

    def name(self) -> Text:
        return "action_save_sid"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender_id = tracker.sender_id
        if db.has_sid(sender_id):
            return []
        message = tracker.latest_message.get('text')
        db.set_sid(sender_id, message)
        dispatcher.utter_message(text='Ok! Giờ tớ đã sẵn sàng trợ giúp cậu xem thời khóa biểu')
        return []