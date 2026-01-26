from .base import BaseAgent
from .deep_search import DeepSearchAgent
from .formulation import FormulationAgent
from .stability import StabilityAgent
from .documentation import DocumentationAgent
from ..models.state import SharedState

class Orchestrator(BaseAgent):
    def __init__(self, state: SharedState, llm, search_client):
        super().__init__("Orchestrator", state, llm)
        self.output_state = state
        self.search_client = search_client
        
        # Initialize sub-agents
        self.deep_search_agent = DeepSearchAgent(state, llm, search_client)
        self.formulation_agent = FormulationAgent(state, llm)
        self.stability_agent = StabilityAgent(state, llm)
        self.documentation_agent = DocumentationAgent(state, llm)

    async def run_workflow(self, user_input: str):
        self.state.meta_memory["user_input"] = user_input
        self.log("Start", "Workflow initiated")

        # Step 1: Parse Brief (Usually part of Orchestrator or a specific Intake Agent)
        await self._parse_brief(user_input)
        self.state.workflow_stage = "research"

        # Step 2: Deep Search
        if self.state.workflow_stage == "research":
            self.log("Transition", "Starting Deep Search")
            await self.deep_search_agent.run()
            self.state.workflow_stage = "formulate"

        # Step 3: Formulation
        if self.state.workflow_stage == "formulate":
            self.log("Transition", "Starting Formulation")
            await self.formulation_agent.run()
            self.state.workflow_stage = "evaluate"

        # Step 4: Stability Check
        if self.state.workflow_stage == "evaluate":
            self.log("Transition", "Starting Stability Analysis")
            await self.stability_agent.run()
            
            # Simple logic: if critical risks, loop back (conceptually)
            # For this MVP, we proceed with warnings
            self.state.workflow_stage = "finalize"

        # Step 5: Documentation
        if self.state.workflow_stage == "finalize":
            self.log("Transition", "Generating Documentation")
            await self.documentation_agent.run()
            self.log("Complete", "Workflow finished")

    async def _parse_brief(self, user_input: str):
        self.log("Action", "Parsing Product Brief from input")
        
        system_prompt = """You are an expert cosmetic product manager. Extract a structured product brief from the user request.
        Return JSON STRICTLY matching this schema:
        {
            "product_type": "string",
            "target_audience": "string",
            "key_benefits": ["string"],
            "texture_preference": "string (defaults to 'Standard' if not specified)",
            "packaging_type": "string (defaults to 'Standard' if not specified)",
            "claims": ["string"],
            "constraints": ["string"]
        }
        """
        
        # In a real scenario, we'd pass the schema to the LLM
        brief_data = await self.llm.generate_json(system_prompt, user_input)
        
        # Fill defaults if missing to be robust
        if "texture_preference" not in brief_data: brief_data["texture_preference"] = "Standard"
        if "packaging_type" not in brief_data: brief_data["packaging_type"] = "Standard"
        if "claims" not in brief_data: brief_data["claims"] = []
        if "constraints" not in brief_data: brief_data["constraints"] = []
        
        from ..models.domain import ProductBrief
        self.state.brief = ProductBrief(**brief_data)
        self.log("Result", f"Brief created: {self.state.brief.product_type}")

    async def run(self):
        pass
