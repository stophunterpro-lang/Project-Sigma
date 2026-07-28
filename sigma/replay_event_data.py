from datetime import datetime

from sigma.replay_event import ReplayEventType


class ReplayEvent:
    def __init__(
        self,
        event_id,
        event_type,
        timestamp,
        order=None,
        order_id=None,
    ):
        if not isinstance(event_type, ReplayEventType):
            raise TypeError(
                f"event_type must be ReplayEventType, got {type(event_type)}"
            )

        if not isinstance(timestamp, datetime):
            raise TypeError(
                f"timestamp must be datetime, got {type(timestamp)}"
            )

        if event_type == ReplayEventType.NEW_ORDER and order is None:
            raise ValueError("NEW_ORDER event requires order")

        if event_type == ReplayEventType.CANCEL_ORDER and order_id is None:
            raise ValueError("CANCEL_ORDER event requires order_id")

        self.event_id = event_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.order = order
        self.order_id = order_id

    def __repr__(self):
        return (
            f"ReplayEvent("
            f"id={self.event_id}, "
            f"type={self.event_type.value}, "
            f"timestamp={self.timestamp}, "
            f"order_id={self.order_id})"
        )