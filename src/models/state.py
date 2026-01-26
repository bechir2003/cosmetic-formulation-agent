from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .domain import ProductBrief, Formula, Evidence, RiskAssessment

class AgentLog(BaseModel):
    agent_name: str
    action: str
    details: str
    timestamp: float

class SharedState(BaseModel):
    brief: Optional[ProductBrief] = None
    research_queries: List[str] = Field(default_factory=list)
    evidence_pool: List[Evidence] = Field(default_factory=list)
    current_formula: Optional[Formula] = None
    stability_risks: List[RiskAssessment] = Field(default_factory=list)
    workflow_stage: str = Field(default="init", description="init, research, formulate, evaluate, finalize")
    logs: List[AgentLog] = Field(default_factory=list)
    meta_memory: Dict[str, Any] = Field(default_factory=dict, description="Temporary scratchpad for agents")

    def log(self, agent: str, action: str, details: str):
        import time
        self.logs.append(AgentLog(
            agent_name=agent,
            action=action,
            details=details,
            timestamp=time.time()
        ))
