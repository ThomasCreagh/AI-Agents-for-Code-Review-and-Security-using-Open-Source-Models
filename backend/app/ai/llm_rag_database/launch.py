from smolagents import OpenAIServerModel, CodeAgent, ToolCallingAgent, HfApiModel, tool, GradioUI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import logging
from typing import Any, Optional

from app.ai.llm_rag_database.model_management.manager import ModelManager
from app.core.config import settings


@tool
def rag_with_reasoner(user_query: str, vectordb: Chroma, reasoner: CodeAgent) -> str:
    """
    RAG tool that performs retrieval and generates responses using the reasoning model.

    Args:
        user_query: The user's question to query the vector database with.
        vectordb: The vector database instance to search in.
        reasoner: The reasoning agent to use for generating responses.

    Returns:
        str: The generated response in Markdown format.
    """
    docs = vectordb.similarity_search(user_query, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""Based on the following context, answer the user's question. Be concise and specific.
    If there isn't sufficient information, give as your answer a better query to perform RAG with.
    Give the response back in a MarkDown Format so it can be displayed nicely.
    
Context:
{context}

Question: {user_query}

Answer:"""

    response = reasoner.run(prompt, reset=False)
    return response


class RunModel:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.model_manager = ModelManager()
        self.huggingface_api_token = settings.HUGGINGFACE_API_TOKEN

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.vectordb = Chroma(
            persist_directory=self.db_dir,
            embedding_function=self.embeddings
        )

        self.init_agents()

    def get_model(self, model_id: str) -> Any:
        """Get a model instance based on the configuration."""
        self.model_config = self.model_manager.get_model_config(model_id)

        if settings.USE_HUGGINGFACE == "yes":
            self.logger.info(f"Initializing HuggingFace model: {model_id}")
            return HfApiModel(
                model_id=model_id,
                token=self.huggingface_api_token
            )
        elif settings.USE_HUGGINGFACE == "no":
            self.logger.info(f"Initializing Ollama model: {model_id}")
            return OpenAIServerModel(
                model_id=model_id,
                api_base="http://localhost:11434/v1",
                api_key="ollama"
            )
        else:
            raise ValueError(
                "USE_HUGGINGFACE env config is not defined correctly")

    def switch_models(self, reasoning_model: Optional[str] = None, tool_model: Optional[str] = None) -> bool:
        """Switch either or both models at runtime."""
        success = True

        if reasoning_model:
            model_switch = self.model_manager.switch_reasoning_model(
                reasoning_model)
            if model_switch:
                self.logger.info(
                    f"Switching reasoning model to: {reasoning_model}")
                reasoning_model_instance = self.get_model(
                    self.model_manager.current_reasoning_model)
                self.reasoner = CodeAgent(
                    tools=[],
                    model=reasoning_model_instance,
                    add_base_tools=False,
                    max_steps=2
                )
            success = success and model_switch

        if tool_model:
            model_switch = self.model_manager.switch_tool_model(tool_model)
            if model_switch:
                self.logger.info(f"Switching tool model to: {tool_model}")
                tool_model_instance = self.get_model(
                    self.model_manager.current_tool_model)
                self.primary_agent = ToolCallingAgent(
                    tools=[rag_with_reasoner],  # Using the standalone function
                    model=tool_model_instance,
                    add_base_tools=False,
                    max_steps=3
                )
            success = success and model_switch

        return success

    def init_agents(self) -> None:
        try:
            self.reasoning_model = self.get_model(
                self.model_manager.current_reasoning_model)
            self.reasoner = CodeAgent(
                tools=[],
                model=self.reasoning_model,
                add_base_tools=False,
                max_steps=2
            )

            self.tool_model = self.get_model(
                self.model_manager.current_tool_model)
            self.primary_agent = ToolCallingAgent(
                tools=[rag_with_reasoner],  # Using the standalone function
                model=self.tool_model,
                add_base_tools=False,
                max_steps=3
            )

        except Exception as e:
            self.logger.error(f"Error initializing agents: {str(e)}")
            raise

    def run_rag(self, user_query: str) -> str:
        """Execute RAG query using the standalone function."""
        return rag_with_reasoner(user_query, self.vectordb, self.reasoner)

    def main(self) -> None:
        try:
            GradioUI(self.primary_agent).launch()
        except Exception as e:
            self.logger.error(f"Error launching Gradio UI: {str(e)}")
            raise
