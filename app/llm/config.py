from dataclasses import dataclass

#gemini-3.5-flash
#gemini-flash-latest
@dataclass
class LLMConfig:
    provider: str
    api_key: str
    model_name: str = "gemini-3.5-flash"
    temperature: float = 0.0
    max_tokens: int | None = None
    timeout: int | None = None