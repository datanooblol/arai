from arai.agents.base import OfflineAgent
from typing import Dict, Any

class JargonExtractor(OfflineAgent):
    def __init__(self):
        super().__init__()
    
    def __call__(self, user_input:str, **kwargs:Dict[str, Any])->Dict[str, Any]:
        return self.forward(user_input, **kwargs)
    
    def forward(self, user_input:str, **kwargs:Dict[str, Any])->Dict[str, Any]:
        self.target = "query_rewriter"
        response = "JargonExtractor responding..."
        print(response)
        return {"response": response}