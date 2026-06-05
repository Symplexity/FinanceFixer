from enum import Enum

from collections import defaultdict


class EventBus:
    """
    A simple event bus implementation.

    A listener "subscribes" to an event by providing a callback function. All callbacks for the same
    event **must** have the same signature.

    When an event is "published", all callbacks subscribed to that event are called with the provided data.
    """

    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event: Events, callback):
        """
        Subscribe to an event. Callbacks for the same event must have the same signature.

        :param event: The name of the event to subscribe to.
        :param callback: The callback function to call when the event is published.

        """
        self._subscribers[event].append(callback)

    def publish(self, event: Events, **data):
        """
        Publish an event. All callbacks subscribed to this event will be called with the provided
        data.

        :param event: The name of the event to publish.
        :param data: The data to pass to the callbacks.
        """
        for callback in self._subscribers[event]:
            callback(**data)


class Events(Enum):
    ADD_LOAN = "add_loan"
    GET_LOAN = "get_loan"
    DELETE_LOAN = "delete_loan"
    EDIT_LOAN = "edit_loan"
    SHOW_MESSAGE = "show_message"
    REFRESH_LOANS = "refresh_loans"
