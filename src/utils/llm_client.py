import os
import json
import httpx
from typing import Dict, Any, List
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        http_client = httpx.AsyncClient(verify=False)
        self.client = AsyncOpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_API_BASE"),
            http_client=http_client
        )
        self.model = "hosted_vllm/Llama-3.1-70B-Instruct" 

    async def generate_json(self, system_prompt: str, user_prompt: str, schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generates a JSON response from the LLM.
        """
        try:
            # Force JSON mode / instruction
            enhanced_system_prompt = f"{system_prompt}\n\nIMPORTANT: You must return valid JSON only. Do not wrap in markdown blocks like ```json."
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": enhanced_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2, # Low temperature for consistent JSON
                max_tokens=2048,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # Simple cleanup if the model still adds markdown
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            elif "```" in content:
                content = content.replace("```", "")
                
            return json.loads(content.strip())
        except Exception as e:
            print(f"LLM Error (JSON): {e}")
            return {}

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error (Text): {e}")
            return f"Error generating text: {e}"


