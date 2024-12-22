from arai.agents.base import OnlineAgent

class InputAgent(OnlineAgent):
    def start_conversation(self, user_input:str):
        self.log(f"Processing input: {user_input}")
        response = {
            "user_input":user_input,
            **self.get_event_metadata()
        }
        self.event_bus.publish(event_type="input_received", event_data=response)