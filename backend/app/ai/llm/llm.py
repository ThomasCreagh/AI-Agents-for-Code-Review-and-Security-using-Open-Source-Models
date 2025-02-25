import os
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from app.core.config import settings

def initialise_llm(model: str = None):
    """
    Initialize the LLM based on configuration.
    If USE_ANTHROPIC is true, use Claude API, otherwise use Ollama.
    """
    use_anthropic = os.getenv("USE_ANTHROPIC", "false").lower() == "true"
    
    if use_anthropic:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required when USE_ANTHROPIC is true")
        
        anthropic_model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        print(f"Using Anthropic Claude API with model: {anthropic_model}")
        return ChatAnthropic(
            anthropic_api_key=api_key,
            model=anthropic_model,
            temperature=0
        )
    else:
        ollama_model = model or os.getenv("LLM_MODEL", "granite3.1-dense:2b")
        base_url = os.getenv("LLM_BASE_URL", "http://ollama:11434")
        print(f"Using Ollama with model: {ollama_model} at {base_url}")
        return ChatOllama(
            base_url=base_url,
            model=ollama_model,
            temperature=0
        )