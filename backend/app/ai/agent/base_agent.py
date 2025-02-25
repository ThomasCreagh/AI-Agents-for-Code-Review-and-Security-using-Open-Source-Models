from ..workflow.graph_config import create_security_rag_graph
from ..llm.llm import initialise_llm
from ..database.init_chroma import initialize_vector_store
from app.core.config import settings

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

class BaseAgent:
    def __init__(self, vector_store=None):
        self.llm = initialise_llm()

        if vector_store is None:
            self.vector_store = initialize_vector_store(
                "nomic-embed-text", "general_docs")
        else:
            self.vector_store = vector_store

        self.memory = MemorySaver()

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
                initial_state = {
                    "messages": [],
                    "latest_user_message": message,
                    "context": {}
                }

                result = self.graph.invoke(initial_state, self.config)
                self.state = result
            else:
                result = self.graph.invoke(
                    Command(resume=message),
                    self.config
                )
                self.state = result

            ai_messages = [
                msg for msg in result["messages"] if msg.type == "ai"]

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