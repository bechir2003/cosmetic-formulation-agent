import os
import httpx
from typing import List, Dict, Any

class SearchResult:
    def __init__(self, url: str, title: str, snippet: str, source_type: str = "web"):
        self.url = url
        self.title = title
        self.snippet = snippet
        self.source_type = source_type

class SearchClient:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")

    async def search(self, query: str) -> List[SearchResult]:
        """
        Performs applied search for the given query.
        """
        print(f"  [SearchClient] Searching for: '{query}'...")
        
        results = []
        try:
            # Using serpapi via simple HTTP request for async compatibility without extra overhead
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://serpapi.com/search",
                    params={
                        "api_key": self.api_key,
                        "q": query,
                        "engine": "google"
                    }
                )
                data = resp.json()
                
                # Check for organic results
                if "organic_results" in data:
                    for item in data["organic_results"][:5]: # Top 5
                        results.append(SearchResult(
                            url=item.get("link", ""),
                            title=item.get("title", ""),
                            snippet=item.get("snippet", ""),
                            source_type="web" # General web for now
                        ))
        except Exception as e:
            print(f"Search API Error: {e}")
            
        return results
