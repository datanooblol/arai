from typing import List
from abc import ABC, abstractmethod
from arai.variables.model import BroModel

class BaseProfile(ABC):
    @abstractmethod
    def as_prompt(self)->str:
        pass

class PersonalInfo(BaseProfile):
    def __init__(
            self,
            name:str=None,
            persona:str=None,
            background:str=None,
            experiences:List[str]=None
    ):
        self.name = name
        self.persona = persona
        self.background = background
        self.experiences = experiences

    def get_name(self):
        if isinstance(self.name, str) and self.name is not None:
            return f"Name: {self.name}"
        return ""
    
    def get_persona(self):
        if isinstance(self.persona, str) and self.persona is not None:
            return f"Persona: {self.persona}"
        return ""
    
    def get_background(self):
        if isinstance(self.background, str) and self.background is not None:
            return f"Background: \n{self.background}"
        return ""
    
    def get_experiences(self):
        if isinstance(self.experiences, list) and self.experiences is not None:
            return "Experiences: \n\t- "+"\n\t- ".join(self.experiences)
        return ""
    
    def as_prompt(self):
        return f"{self.get_name()}\n\n{self.get_persona()}\n\n{self.get_background()}\n\n{self.get_experiences()}".strip()

class JobDescription(BaseProfile):
    def __init__(
            self, 
            job_title:str, 
            job_description:List[str],
            outcomes:BroModel=None
    ):
        self.job_title = job_title
        self.job_description = job_description
        self.outcomes:BroModel = outcomes
    
    def get_job_title(self):
        return f"Job Title: {self.job_title}"
    
    def get_job_description(self):
        return "Job Desciptions: \n\t- "+"\n\t- ".join(self.job_description)
    
    def get_outcomes(self):
        if issubclass(self.outcomes, BroModel) and self.outcomes is not None:
            return self.outcomes.as_prompt()

    def as_prompt(self):
        return f"{self.get_job_title()}\n\n{self.get_job_description()}\n\n{self.get_outcomes()}".strip()
    
class AgentProfile(BaseProfile):
    def __init__(self, info:PersonalInfo, jd:JobDescription):
        self.info = info
        self.jd = jd
        
    def as_prompt(self):
        return f"{self.info.as_prompt()}\n\n{self.jd.as_prompt()}".strip()