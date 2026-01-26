import asyncio
import os
from src.models.state import SharedState
from src.utils.llm_client import LLMClient
from src.tools.search_client import SearchClient
from src.agents.orchestrator import Orchestrator

async def main():
    print("Initializing Cosmetic Formulation Agent System...")
    
    # 1. Setup Infrastructure
    # In a real run, load API keys from environment
    # Switched to "real" provider to use hosted VLLM and SerpAPI
    llm_client = LLMClient()
    search_client = SearchClient()
    
    # 2. Initialize State
    state = SharedState()
    
    # 3. Initialize Orchestrator
    orchestrator = Orchestrator(state, llm_client, search_client)
    
    # 4. User Input (Simulated interactive loop)
    user_input = "Develop a rich barrier repair cream for dry skin using ceramides and natural emulsifiers."
    print(f"\nIncoming Request: '{user_input}'\n")
    
    # 5. Run Workflow
    await orchestrator.run_workflow(user_input)
    
    print("\nSystem execution completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
