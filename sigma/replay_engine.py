from sigma.matching_engine import MatchingEngine
from sigma.replay_event import ReplayEventType
from sigma.replay_event_data import ReplayEvent


class ReplayEngine:
    def __init__(self):
        self.matching_engine = MatchingEngine()
        self.events = []

    def add_event(self, event):
        if not isinstance(event, ReplayEvent):
            raise TypeError(
                f"event must be ReplayEvent, got {type(event)}"
            )

        self.events.append(event)

    def run(self):
        sorted_events = sorted(
            self.events,
            key=lambda event: (
                event.timestamp,
                event.event_id,
            ),
        )

        for event in sorted_events:
            if event.event_type == ReplayEventType.NEW_ORDER:
                self.matching_engine.process_order(event.order)

            elif event.event_type == ReplayEventType.CANCEL_ORDER:
                self.matching_engine.cancel_order(event.order_id)

    def get_matching_engine(self):
        return self.matching_engine