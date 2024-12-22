from typing import Callable
from arai.agents.base import OfflineAgent
from arai.agents.profile import AgentProfile, JobDescription, PersonalInfo
from arai.utils.llm_utils import llm_wrapper
from arai.variables.model import BroModel

class Summary(BroModel):
    summary:str = BroModel(description="Summary of the first page to lay a background of the paper.", default="This paper is about...")

profile = AgentProfile(
    info=PersonalInfo(
        background="Decades of experience in summarizing research papers.",
    ),
    jd=JobDescription(
        job_title="FirstPageSummarizer",
        job_description=[
            "Read the first page of the document carefully.",
            "Summarize the first page of the document.",
            "In summary, include the research problem, research question, and the main objective of the paper.",
            "In summary, include methodology, results, and conclusion of the paper.",
            "Remember do not make up any information. Only summarize the information that is present in the first page.",
            "Return only the summary of the first page."
        ],
        outcomes=Summary
    )
)

class FirstPageSummarizer(OfflineAgent):
    def __init__(self, profile:AgentProfile=profile, llm:Callable=llm_wrapper):
        super().__init__()
        self.event_bus.subscribe("summary_needed", self.run)
        self.profile = profile

    def run(self, event_data:dict):
        first_page = event_data.get("first_page", "")
        self.log(f"Summarizing first page...")
        prompt = self.profile.as_prompt()
        prompt += f"\n\nFirst Page: \n{first_page}"
        outcomes = self.profile.jd.outcomes
        response:Summary = self.retry_parsing(prompt, outcomes)
        self.event_bus.publish("end", {"summary": response.summary})