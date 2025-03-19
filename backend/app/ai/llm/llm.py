import os
import time
import tiktoken
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from app.core.config import settings

# Utility to count tokens
def count_tokens(text):
    encoder = tiktoken.get_encoding("cl100k_base")  # Claude uses cl100k
    return len(encoder.encode(text))

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
        
        # Default to faster model for most operations
        default_model = "claude-3-haiku-20240307"
        anthropic_model = model or os.getenv("ANTHROPIC_MODEL", default_model)
        print(f"Using Anthropic Claude API with model: {anthropic_model}")
        
        time.sleep(1)  # Prevent rate limiting
        
        return ChatAnthropic(
            anthropic_api_key=api_key,
            model=anthropic_model,
            temperature=0,
            timeout=30,  # timeout
            max_retries=2,  # basic retry
            max_tokens=1000,  # Limit output tokens to avoid cutoffs
            max_tokens_to_sample=1000
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