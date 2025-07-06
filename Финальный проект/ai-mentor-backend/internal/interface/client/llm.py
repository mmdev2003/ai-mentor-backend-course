from abc import abstractmethod
from typing import Protocol

from internal import model

class ILLMClient(Protocol):
    @abstractmethod
    async def generate(
            self,
            history: list[model.Message],
            system_prompt: str = "",
            temperature: float = 0.5,
            llm_model: str = "gpt-4o-mini",
            base64img: str = None
    ) -> str: pass
