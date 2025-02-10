from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# Default models from environment variables with fallbacks
DEFAULT_REASONING_MODEL = os.getenv("REASONING_MODEL_ID", "deepseek-r1:7b-8k")
DEFAULT_TOOL_MODEL = os.getenv("TOOL_MODEL_ID", "qwen2.5:14b-instruct-q4_K_M")

# Comprehensive model configurations
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "deepseek-r1:7b-8k": {
        "type": "reasoning",
        "provider": "ollama",
        "context_length": 8192,
        "default_temp": 0.7,
        "description": "DeepSeek Coder model for reasoning tasks",
        "capabilities": ["code generation", "reasoning", "analysis"]
    },
    "qwen2.5:14b-instruct-q4_K_M": {
        "type": "tool",
        "provider": "ollama",
        "context_length": 8192,
        "default_temp": 0.7,
        "description": "Qwen model for tool coordination",
        "capabilities": ["instruction following", "tool use", "coordination"]
    },
}

# Validation and error messages
ERROR_MESSAGES = {
    "model_not_found": "Model {model_name} not found in configurations",
    "invalid_model_type": "Model {model_name} is not a valid {required_type} model",
    "initialization_failed": "Failed to initialize {model_name}: {error}",
    "switch_failed": "Failed to switch to {model_name}: {error}"
}