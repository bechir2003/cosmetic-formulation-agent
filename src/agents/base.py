from abc import ABC, abstractmethod
from ..models.state import SharedState
from ..utils.llm_client import LLMClient

class BaseAgent(ABC):
    def __init__(self, name: str, state: SharedState, llm: LLMClient):
        self.name = name
        self.state = state
        self.llm = llm

    @abstractmethod
    async def run(self) -> SharedState:
        """
        Executes the agent's logic and updates the shared state.
        """
        pass

    def log(self, action: str, details: str):
        self.state.log(self.name, action, details)
        print(f"[{self.name}] {action}: {details}")
