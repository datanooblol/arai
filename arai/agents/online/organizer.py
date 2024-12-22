from arai.agents.base import OnlineAgent
from typing import Dict, Any, Callable
from arai.agents.profile import PersonalInfo, JobDescription, AgentProfile
from arai.utils.llm_utils import llm_wrapper
from arai.variables.model import BroModel, BroField

class Router(BroModel):
    event_type:str = BroField(description="select an event type based on Job Descriptions", default="event_type_selected")
    reason:str = BroField(description="reason for choosing this event", default="selecting this event is because of ...")

input_received = AgentProfile(
    info=PersonalInfo(),
    jd=JobDescription(
        job_title="Organizer",
        job_description=[
            "Read INPUT carefully, think which action is the best match. Return only the name of the target agent.",
            "If INPUT contains jargons, abbreviations, or acronyms, return 'jargon_needed'.",
            "If INPUT does not contain jargons, abbreviations, or acronyms, return 'query_needed'.",
        ],
        outcomes=Router
    )
)

query_rewritten = None
documents_ready = None
documents_rejected = None

profiles = {
    "input_received": input_received,
    "query_rewritten": query_rewritten,
    "documents_ready": documents_ready,
    "documents_rejected": documents_rejected
}

class OrganizerAgent(OnlineAgent):
    def __init__(self, profiles:Dict[str, AgentProfile]=profiles, llm:Callable=llm_wrapper):
        super().__init__()
        self.llm = llm
        self.profiles:Dict[str, AgentProfile] = profiles
        for event_type in self.profiles.keys():
            self.event_bus.subscribe(event_type, self.run)

    def run_event_input_received(self, event_type:str, event_data:Dict[str, Any]):
        user_input = event_data.get("user_input", "")
        self.log(f"Routing request...")
        profile = self.profiles[event_type]
        prompt = profile.as_prompt()
        prompt += f"\n\nINPUT:\n\n{user_input}\n\n"
        outcomes = profile.jd.outcomes
        response = self.retry_parsing(prompt, outcomes)

        if isinstance(response, str):
            event_type = "query_needed"
            reason = "parsed unsuccessfully"
        else:
            event_type = response.event_type
            reason = response.reason
        event_data = {
            "user_input": user_input,
            "reason": reason,
            **self.get_event_metadata()
        }

        return event_type, event_data

    def run_event_query_rewritten(self, event_type:str, event_data:Dict[str, Any]):
        user_input = event_data.get("user_input", "")
        self.log(f"Routing to QueryDecomposer...")
        event_data = {
            "user_input": user_input,
            **self.get_event_metadata()
        }
        return "query_needed", event_data

    def run_event_documents_ready(self, event_type:str, event_data:Dict[str, Any]):
        documents = event_data.get("documents", [])
        self.log(f"Routing to AnswerGenerator...")
        event_data = {
            documents: documents,
            **self.get_event_metadata()
        }
        return "answer_needed", event_data

    def run_event_documents_rejected(self, event_type:str, event_data:Dict[str, Any]):
        reason = event_data.get("reason", "")
        self.log(f"Routing to BadNewsDeliver...")
        event_data = {
            "reason": reason,
            **self.get_event_metadata()
        }
        return "human_in_the_loop_needed", event_data

    def run(self, event_data:dict):
        event_type = event_data.get("event_type", "")
        if event_type=="input_received":
            event_type, response = self.run_event_input_received(event_type, event_data)
        if event_type=="query_rewritten":
            event_type, response = self.run_event_query_rewritten(event_type, event_data)
        if event_type=="documents_ready":
            event_type, response = self.run_event_documents_ready(event_type, event_data)
        if event_type=="documents_rejected":    
            event_type, response = self.run_event_documents_rejected(event_type, event_data)

        self.event_bus.publish(event_type=event_type, event_data=response)
        return response