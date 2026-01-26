from .base import BaseAgent
from ..models.state import SharedState
from ..models.domain import RiskAssessment
from ..utils.llm_client import LLMClient

class StabilityAgent(BaseAgent):
    def __init__(self, state: SharedState, llm: LLMClient):
        super().__init__("Stability", state, llm)

    async def run(self):
        self.log("Action", "Analyzing formula for stability and compatibility risks")
        
        system_prompt = """You are a quality assurance chemist. Analyze this formula for stability risks (pH drift, separation, oxidization, incompatibility).
        Return JSON STRICTLY matching this schema:
        {
            "risks": [
                {
                    "risk_level": "low" | "medium" | "high" | "critical",
                    "category": "stability" | "compatibility" | "safety" | "regulatory",
                    "description": "string",
                    "mitigation_strategy": "string"
                }
            ]
        }
        IMPORTANT: 'category' must be EXACTLY one of 'stability', 'compatibility', 'safety', or 'regulatory'. Do not use specific types like 'oxidation' as the category name, put that in description.
        """
        user_prompt = f"Formula: {self.state.current_formula.model_dump_json()}"
        
        response = await self.llm.generate_json(system_prompt, user_prompt)
        risks_data = response.get("risks", [])
        
        valid_categories = ["stability", "compatibility", "safety", "regulatory"]
        
        for r in risks_data:
            # Robustness correction for LLM outputs
            if "category" in r:
                cat = r["category"].lower()
                if cat not in valid_categories:
                    if cat in ["oxidation", "separation", "ph drift", "microbial", "structure"]:
                        r["category"] = "stability"
                    elif cat in ["irritation", "toxicity", "allergen"]:
                        r["category"] = "safety"
                    elif cat in ["incompatibility", "solubility"]:
                        r["category"] = "compatibility"
                    else:
                        # Fallback
                        r["category"] = "stability"
                        
            self.state.stability_risks.append(RiskAssessment(**r))
            
        self.log("Result", f"Identified {len(self.state.stability_risks)} potential risks.")
