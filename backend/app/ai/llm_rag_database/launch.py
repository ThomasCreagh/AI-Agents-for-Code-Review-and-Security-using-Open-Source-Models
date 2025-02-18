from smolagents import OpenAIServerModel, CodeAgent, ToolCallingAgent, HfApiModel, tool, GradioUI
# from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import logging

from app.ai.llm_rag_database.model_management.manager import ModelManager
from app.ai.llm_rag_database.model_management.config import DEFAULT_REASONING_MODEL, DEFAULT_TOOL_MODEL
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables and initialize model manager
# load_dotenv()
model_manager = ModelManager()

# Initialize environment variables
huggingface_api_token = settings.HUGGINGFACE_API_TOKEN


def get_model(model_id):
    """
    Get a model instance based on the configuration and environment settings.
    Supports both HuggingFace and Ollama models.
    """
    using_huggingface = settings.USE_HUGGINGFACE
    model_config = model_manager.get_model_config(model_id)

    if using_huggingface:
        logger.info(f"Initializing HuggingFace model: {model_id}")
        return HfApiModel(
            model_id=model_id,
            token=huggingface_api_token
        )
    else:
        logger.info(f"Initializing Ollama model: {model_id}")
        return OpenAIServerModel(
            model_id=model_id,
            api_base="http://localhost:11434/v1",
            api_key="ollama"
        )


def switch_models(reasoning_model: str = None, tool_model: str = None):
    """
    Switch either or both models at runtime.
    Returns True if all requested switches were successful.
    """
    success = True

    if reasoning_model:
        model_switch = model_manager.switch_reasoning_model(reasoning_model)
        if model_switch:
            logger.info(f"Switching reasoning model to: {reasoning_model}")
            reasoning_model_instance = get_model(
                model_manager.current_reasoning_model)
            global reasoner
            reasoner = CodeAgent(
                tools=[],
                model=reasoning_model_instance,
                add_base_tools=False,
                max_steps=2
            )
        success = success and model_switch

    if tool_model:
        model_switch = model_manager.switch_tool_model(tool_model)
        if model_switch:
            logger.info(f"Switching tool model to: {tool_model}")
            tool_model_instance = get_model(model_manager.current_tool_model)
            global primary_agent
            primary_agent = ToolCallingAgent(
                tools=[rag_with_reasoner],
                model=tool_model_instance,
                add_base_tools=False,
                max_steps=3
            )
        success = success and model_switch

    return success


# Initialize vector store and embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'}
)
db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
vectordb = Chroma(persist_directory=db_dir, embedding_function=embeddings)


@tool
def rag_with_reasoner(user_query: str) -> str:
    """
    RAG tool that performs retrieval and generates responses using the reasoning model.

    Args:
        user_query: The user's question to query the vector database with.
    """
    # Search for relevant documents
    docs = vectordb.similarity_search(user_query, k=3)

    # Combine document contents
    context = "\n\n".join(doc.page_content for doc in docs)

    # Create prompt with context
    prompt = f"""Based on the following context, answer the user's question. Be concise and specific.
    If there isn't sufficient information, give as your answer a better query to perform RAG with.
    
Context:
{context}

Question: {user_query}

Answer:"""

    # Get response from reasoning model
    response = reasoner.run(prompt, reset=False)
    return response


# Initialize the agents with default models
try:
    # Initialize reasoning agent
    reasoning_model = get_model(model_manager.current_reasoning_model)
    reasoner = CodeAgent(
        tools=[],
        model=reasoning_model,
        add_base_tools=False,
        max_steps=2
    )

    # Initialize tool calling agent
    tool_model = get_model(model_manager.current_tool_model)
    primary_agent = ToolCallingAgent(
        tools=[rag_with_reasoner],
        model=tool_model,
        add_base_tools=False,
        max_steps=3
    )

except Exception as e:
    logger.error(f"Error initializing agents: {str(e)}")
    raise


def main():
    """
    Main function to launch the Gradio UI interface.
    """
    try:
        GradioUI(primary_agent).launch()
    except Exception as e:
        logger.error(f"Error launching Gradio UI: {str(e)}")
        raise
