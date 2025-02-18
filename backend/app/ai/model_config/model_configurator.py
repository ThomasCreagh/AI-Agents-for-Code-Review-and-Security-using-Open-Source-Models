"""
Flexible LLM Integration with Multiple Provider Support

This module provides a configurable wrapper for various LLM providers using LiteLLM.
It includes support for multiple providers (Ollama, OpenAI, Anthropic, etc.) and
implements a security analysis chain using LangChain. The implementation follows
best practices for LangChain integration with proper field declarations.
"""

from typing import Optional, Dict, Any
import litellm
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables from .env file
# This enables secure configuration management for API keys and other sensitive data
load_dotenv()

class ConfigurableLLMWrapper(LLM, BaseModel):
    """
    A flexible LLM wrapper that supports multiple providers through LiteLLM.
    
    This class provides a unified interface for interacting with different LLM providers
    while handling provider-specific configurations and requirements. It properly
    declares fields using Pydantic for LangChain compatibility.
    
    The class inherits from both LLM (for LangChain integration) and BaseModel
    (for Pydantic field validation and serialization).
    """
    
    # Declare required fields using Pydantic Field class
    model_name: str = Field(..., description="Name of the model to use")
    provider: str = Field(default="ollama", description="Provider name (e.g., ollama, openai, anthropic)")
    api_base: Optional[str] = Field(default=None, description="Base URL for API calls")
    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    additional_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Additional provider-specific parameters")

    class Config:
        """Pydantic configuration class"""
        arbitrary_types_allowed = True

    def __init__(
        self,
        model_name: str,
        provider: str = "ollama",
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the LLM wrapper with specific provider configuration.
        
        Args:
            model_name: Name of the model to use
            provider: Provider name (default: "ollama")
            api_base: Base URL for API calls (optional)
            api_key: API key for authentication (optional)
            **kwargs: Additional provider-specific parameters
        """
        # Initialize both parent classes
        super().__init__(
            model_name=model_name,
            provider=provider,
            api_base=api_base,
            api_key=api_key,
            additional_kwargs=kwargs
        )
        
        # Set up provider-specific configurations
        self._configure_provider()

    def _configure_provider(self):
        """
        Configure provider-specific settings and API details.
        
        This method sets up the necessary configurations for each supported provider,
        including API bases and authentication details. It reads from environment
        variables when appropriate.
        """
        # Define configuration templates for each provider
        provider_configs = {
            "ollama": {
                "api_base": self.api_base or "http://localhost:11434/v1",
                "api_key": "ollama"  # Ollama's default
            },
            "openai": {
                "api_key": self.api_key or os.getenv("OPENAI_API_KEY")
            },
            "anthropic": {
                "api_key": self.api_key or os.getenv("ANTHROPIC_API_KEY")
            },
            # Add configurations for other providers here as needed
        }

        # Get provider config or empty dict if provider not found
        config = provider_configs.get(self.provider, {})
        
        # Update instance attributes with provider configuration
        for key, value in config.items():
            if value is not None:
                setattr(self, key, value)

    def _call(self, prompt: str, stop: Optional[list] = None, **kwargs) -> str:
        """
        Execute the LLM call through LiteLLM.
        
        This method handles the actual interaction with the language model through
        LiteLLM's unified interface. It properly formats the request and handles
        any provider-specific requirements.
        
        Args:
            prompt: The input text to send to the model
            stop: Optional list of stop sequences
            **kwargs: Additional parameters for the completion call
            
        Returns:
            str: The model's response text
            
        Raises:
            RuntimeError: If there's an error during the LLM call
        """
        try:
            # Prepare messages in the format expected by LiteLLM
            messages = [{"role": "user", "content": prompt}]
            
            # Prepare completion parameters
            completion_params = {
                "model": f"{self.provider}/{self.model_name}",
                "messages": messages,
                "api_base": getattr(self, "api_base", None),
                "api_key": getattr(self, "api_key", None)
            }
            
            # Remove None values from parameters
            completion_params = {k: v for k, v in completion_params.items() if v is not None}
            
            # Add any additional kwargs passed to the instance
            completion_params.update(self.additional_kwargs)
            
            # Make the completion call through LiteLLM
            response = litellm.completion(**completion_params)
            return response.choices[0].message.content
            
        except Exception as e:
            raise RuntimeError(f"Error calling LLM: {str(e)}")

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters of the LLM."""
        return {
            "model_name": self.model_name,
            "provider": self.provider
        }

    @property
    def _llm_type(self) -> str:
        """Get the type identifier for this LLM."""
        return "configurable_litellm"

def create_security_analysis_chain(llm: LLM) -> SequentialChain:
    """
    Create a security analysis chain using the provided LLM.
    
    This function sets up a two-step chain:
    1. Analysis of security vulnerabilities
    2. Generation of a professional report
    
    Args:
        llm: The language model to use for the chain
        
    Returns:
        SequentialChain: A chain that can analyze security issues and generate reports
    """
    # Define the security analysis prompt template
    analyser_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="""You are a security expert. Analyze the following input for security vulnerabilities:
        
        {input_text}
        
        Provide a detailed analysis with potential risks and recommendations."""
    )

    # Define the report generation prompt template
    report_prompt = PromptTemplate(
        input_variables=["analysis_result"],
        template="""Based on the following analysis:
        {analysis_result}

        Generate a professional report summarizing the findings and recommendations. Use the following format:

        ### Professional Security Analysis Report

        - **Summary:**
        - **Findings:**
        - **Recommendations:**"""
    )

    # Create the individual chain components
    analyser_chain = LLMChain(llm=llm, prompt=analyser_prompt, output_key="analysis_result")
    report_chain = LLMChain(llm=llm, prompt=report_prompt, output_key="final_report")

    # Combine into a sequential chain
    return SequentialChain(
        chains=[analyser_chain, report_chain],
        input_variables=["input_text"],
        output_variables=["analysis_result", "final_report"]
    )

def main():
    """
    Main function demonstrating the usage of the security analysis chain
    with different LLM providers.
    """
    # Example configuration for Ollama
    try:
        ollama_llm = ConfigurableLLMWrapper(
            model_name="granite3.1-dense:2b",  # or your chosen model
            provider="ollama",
            api_base="http://localhost:11434"
        )

        # Example configuration for OpenAI 
        # openai_llm = ConfigurableLLMWrapper(
        #     model_name="gpt-3.5-turbo",
        #     provider="openai"
        # )

        # Create the security analysis chain
        security_chain = create_security_analysis_chain(ollama_llm)

        # Example code to analyze
        issue_description = """Check the following code for any security vulnerabilities:

        def connect_to_service():
            API_KEY = "12345-ABCDE-67890-FGHIJ"  # Exposed API Key
            endpoint = "https://example.com/api"
            response = requests.get(endpoint, headers={"Authorization": f"Bearer {API_KEY}"})
            return response.json()

        connect_to_service()"""

        # Run the analysis
        result = security_chain({"input_text": issue_description})
        
        print("\n--- Analysis Report ---\n")
        print(result["analysis_result"])
        
        print("\n--- Final Report ---\n")
        print(result["final_report"])
        
    except Exception as e:
        print(f"Error running security analysis: {str(e)}")

if __name__ == "__main__":
    main()