from .base import BaseAgent
from ..models.state import SharedState
from ..models.domain import Formula, Ingredient
from ..utils.llm_client import LLMClient

class FormulationAgent(BaseAgent):
    def __init__(self, state: SharedState, llm: LLMClient):
        super().__init__("Formulation", state, llm)

    async def run(self):
        self.log("Action", "Synthesizing formula from evidence")
        
        system_prompt = """
        You are a senior cosmetic chemist. Create a detailed formulation based on the product brief and the provided scientific evidence.
        Ensure total percentage is exactly 100%. Assign proper phases and justifications.
        
        Return JSON STRICTLY matching this schema:
        {
            "name": "string",
            "description": "string",
            "form": "string (e.g. O/W Emulsion)",
            "total_percentage": float,
            "ph_target": "string",
            "viscosity_target": "string",
            "ingredients": [
                {
                    "name": "string",
                    "percentage": float,
                    "function": "string",
                    "phase": "string (A, B, C...)",
                    "justification": "string",
                    "supplier": "string (optional)"
                }
            ]
        }
        """
        
        evidence_text = "\n".join([f"- {e.key_finding} (Ref: {e.citation})" for e in self.state.evidence_pool])
        user_prompt = f"""
        Brief: {self.state.brief.model_dump_json()}
        
        Evidence:
        {evidence_text}
        
        Generate the Formula object.
        """
        
        formula_data = await self.llm.generate_json(system_prompt, user_prompt)
        
        # Validate and parse
        self.state.current_formula = Formula(**formula_data)
        self.log("Result", f"Formula '{self.state.current_formula.name}' generated with {len(self.state.current_formula.ingredients)} ingredients.")
