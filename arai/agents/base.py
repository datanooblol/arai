from typing import Callable
from arai.variables.model import BroModel
from arai.memories.events import EventBus, OnlineEventBus, OfflineEventBus
import time

class PubSubAgent:
    def __init__(self):
        self.event_bus = EventBus()
        self.max_retries = 5
        self.llm:Callable = None
    
    def log(self, message:str):
        print(f"{self.__class__.__name__}: {message}")

    def get_event_metadata(self):
        return {
            "source": self.__class__.__name__,
            "timestamp": int(time.time())
        }

    def run(self, **kwargs:dict):
        ...

    def retry_parsing(self, prompt:str, outcomes:BroModel):
        errors = []
        error_msg = ""
        print(f"{self.__class__.__name__}: parsing", end="", flush=False)
        for i in range(self.max_retries+1):
            if len(errors)>0:
                error_msg = "Errors: "
                error_msg += "\n\t-".join(errors)
            response = self.llm(f"{prompt}{error_msg}")
            try:
                response = outcomes.from_json(response)
                break
            except Exception as e:
                errors.append(str(e))
                print(".", end="", flush=False)
                continue
        print("")
        return response
    
class OnlineAgent(PubSubAgent):
    def __init__(self):
        super().__init__()
        self.event_bus = OnlineEventBus()

class OfflineAgent(PubSubAgent):
    def __init__(self):
        super().__init__()
        self.event_bus = OfflineEventBus()