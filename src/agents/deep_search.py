from typing import List
from .base import BaseAgent
from ..models.state import SharedState
from ..models.domain import Evidence
from ..utils.llm_client import LLMClient
from ..tools.search_client import SearchClient

class DeepSearchAgent(BaseAgent):
    def __init__(self, state: SharedState, llm: LLMClient, search_client: SearchClient):
        super().__init__("DeepSearch", state, llm)
        self.search_client = search_client

    async def run(self):
        # 1. Generate Queries
        await self._generate_queries()
        
        # Deduplicate queries to save tokens and time
        self.state.research_queries = list(set(self.state.research_queries))
        
        # Track collected URLs to avoid duplicates in evidence pool
        collected_urls = {e.source_url for e in self.state.evidence_pool}

        # 2. Execute Search & Process Results
        for query in self.state.research_queries:
            self.log("Action", f"Searching: {query}")
            results = await self.search_client.search(query)
            
            # 3. Analyze results -> Evidence (Simulated extraction here)
            for res in results:
                if res.url in collected_urls:
                    continue
                
                # In real app: Feed snippet to LLM to extract key finding & relevance
                # Here: We use the raw data from our mock search client
                
                evidence = Evidence(
                    source_url=res.url,
                    source_type=res.source_type, # type: ignore
                    title=res.title,
                    key_finding=res.snippet,
                    relevance_score=0.9, # Mocked
                    confidence_score=0.85, # Mocked
                    citation=f"{res.title} ({res.url})"
                )
                self.state.evidence_pool.append(evidence)
                collected_urls.add(res.url)
        
        self.log("Result", f"Collected {len(self.state.evidence_pool)} unique pieces of evidence")

    async def _generate_queries(self):
        system_prompt = """You are a research scientist. Generate search queries to find scientific evidence for detailed cosmetic formulation ingredients based on the brief.
        Return JSON STRICTLY matching this schema:
        {
            "queries": ["string"]
        }
        """
        user_prompt = f"Product Brief: {self.state.brief.model_dump_json()}"
        
        response = await self.llm.generate_json(system_prompt, user_prompt)
        self.state.research_queries = response.get("queries", [])
