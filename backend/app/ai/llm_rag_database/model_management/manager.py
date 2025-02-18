from typing import Optional, Dict, Any
import logging
from .config import (
    MODEL_CONFIGS, ERROR_MESSAGES,
    DEFAULT_REASONING_MODEL, DEFAULT_TOOL_MODEL
)


class ModelManager:
    def __init__(self):
        # Initialize with default models from config
        self.current_reasoning_model = DEFAULT_REASONING_MODEL
        self.current_tool_model = DEFAULT_TOOL_MODEL
        self.logger = logging.getLogger(__name__)

    def switch_reasoning_model(self, model_name: str) -> bool:
        """Switch the reasoning model to a different one"""
        if model_name not in MODEL_CONFIGS:
            self.logger.error(
                ERROR_MESSAGES["model_not_found"].format(
                    model_name=model_name))
            return False

        if MODEL_CONFIGS[model_name]["type"] != "reasoning":
            self.logger.error(ERROR_MESSAGES["invalid_model_type"].format(
                model_name=model_name, required_type="reasoning"
            ))
            return False

        self.current_reasoning_model = model_name
        self.logger.info(f"Switched reasoning model to {model_name}")
        return True

    def switch_tool_model(self, model_name: str) -> bool:
        """Switch the tool-calling model to a different one"""
        if model_name not in MODEL_CONFIGS:
            self.logger.error(
                ERROR_MESSAGES["model_not_found"].format(
                    model_name=model_name))
            return False

        if MODEL_CONFIGS[model_name]["type"] != "tool":
            self.logger.error(ERROR_MESSAGES["invalid_model_type"].format(
                model_name=model_name, required_type="tool"
            ))
            return False

        self.current_tool_model = model_name
        self.logger.info(f"Switched tool model to {model_name}")
        return True

    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get the configuration for a specific model"""
        return MODEL_CONFIGS.get(model_name)

    def get_current_models(self) -> Dict[str, str]:
        """Get the currently active models"""
        return {
            "reasoning": self.current_reasoning_model,
            "tool": self.current_tool_model
        }
