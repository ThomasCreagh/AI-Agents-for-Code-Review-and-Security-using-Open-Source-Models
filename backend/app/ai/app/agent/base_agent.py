from langchain_core.messages import HumanMessage
from ..workflow.graph_config import create_security_rag_graph, AgentState
from ..llm.llm import initialise_llm
from ..database.init_chroma import initialize_vector_store
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from dotenv import load_dotenv
import os  

load_dotenv()
class BaseAgent:
    """Base agent that manages the multi-agent security RAG workflow."""
    
    def __init__(self, vector_store=None):
        self.llm = initialise_llm(os.getenv("LLM_MODEL"))
        
        if vector_store is None:
            self.vector_store = initialize_vector_store("nomic-embed-text", "general_docs")
        else:
            self.vector_store = vector_store
        
        # Create a memory saver for persistence
        self.memory = MemorySaver()
        
        # Create the workflow and properly compile it with the checkpointer
        graph = create_security_rag_graph(self.llm, self.vector_store)
        self.graph = graph.compile(checkpointer=self.memory)
        
        self.state = None
        self.config = {
            "configurable": {
                "thread_id": "default_thread"
            }
        }
    
    def process_message(self, message: str) -> str:
        try:
            if self.state is None:
                # First message, initialize the state
                initial_state = {
                    "messages": [],
                    "latest_user_message": message,
                    "context": {}
                }
                
                # Run the graph with initial state
                result = self.graph.invoke(initial_state, self.config)
                self.state = result
            else:
                # For subsequent messages, use Command.resume with the checkpointer
                result = self.graph.invoke(
                    Command(resume=message),
                    self.config
                )
                self.state = result
            
            # Find the AI's response
            ai_messages = [msg for msg in result["messages"] if msg.type == "ai"]
            
            if ai_messages:
                return ai_messages[-1].content
            else:
                return "No response generated."
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error processing message: {str(e)}")
            print(error_trace)
            return f"Error processing message: {str(e)}"