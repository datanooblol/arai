from collections import defaultdict
from typing import Callable
from threading import Lock

class EventBus:
    _instance = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.subscribers = defaultdict(list)
                cls._instance.events = []
        return cls._instance
    
    def subscribe(self, event_type: str, callback: Callable[[dict], None]):
        """Subscribe a callback to a specific event type."""
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, event_data: dict):
        """Notify all subscribers of an event."""
        event_data["event_type"] = event_type
        self.events.append(event_data)
        for callback in self.subscribers.get(event_type, []):
            callback(event_data)

    def resume_from_failure(self):
        """Resume at the last event that failed."""
        event_data = self.get_latest_event()
        event_type = event_data.get("event_type", "")
        for callback in self.subscribers.get(event_type, []):
            callback(event_data)

    def get_events(self):
        return self.events
    
    def get_latest_event(self):
        if len(self.events)>0:
            return self.events[-1]
        return []
    
    def clear_events(self):
        self.events = []
    
    def clear_subscribers(self):
        self.subscribers = defaultdict(list)
    
    def clear_event_bus(self):
        self.clear_events()
        self.clear_subscribers()

class OnlineEventBus(EventBus):
    pass

class OfflineEventBus(EventBus):
    pass