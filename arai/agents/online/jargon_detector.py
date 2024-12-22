from typing import Any, Callable, Dict, List
from arai.agents.base import OnlineAgent
from arai.agents.profile import AgentProfile, JobDescription, PersonalInfo
from arai.utils.llm_utils import llm_wrapper
from arai.variables.model import BroField, BroModel

class Jargon(BroModel):
    jargon:str = BroModel(description="jargon, abbreviation, acronym extracted from INPUT", default="extracted word")

class Jargons(BroModel):
    jargons:List[Jargon] = BroField(description="list of jargons, abbreviations, acronyms extracted from INPUT", default=[
        {"jargon":"extracted jargon"},
        {"jargon":"extracted abbreviation"},
        {"jargon":"extracted acronym"}
    ])

profile = AgentProfile(
    info=PersonalInfo(),
    jd=JobDescription(
        job_title="JargonDetector",
        job_description=[
            "Read INPUT carefully, think which word is a jargon, abbreviation or acronym.",
            "Strategically detect and extract jargons, abbreviations, or acronyms from INPUT.",
            "It is important to extract only the correct jargon, abbreviation, or acronym.",
            "Remember do not extract explanation or description from INPUT.",
        ],
        outcomes=Jargons
    )
)
class JargonDetector(OnlineAgent):
    def __init__(self, profile:AgentProfile=profile, llm:Callable=llm_wrapper):
        super().__init__()
        self.profile = profile
        self.llm = llm
        self.event_bus.subscribe(event_type="jargon_needed", callback=self.run)

    def run(self, event_data:Dict[str, Any]):
        user_input = event_data.get("user_input", "")
        self.log(f"Extracting jargons, abbreviations, acronyms from INPUT...")
        prompt = self.profile.as_prompt()
        prompt += f"\n\nINPUT:\n\n{user_input}\n\n"
        outcomes = self.profile.jd.outcomes
        response = self.retry_parsing(prompt, outcomes)
        event_data = {
            "user_input": user_input,
            "jargons": response.model_dump(),
            **self.get_event_metadata()
        }
        self.event_bus.publish(event_type="editing_needed", event_data=event_data)