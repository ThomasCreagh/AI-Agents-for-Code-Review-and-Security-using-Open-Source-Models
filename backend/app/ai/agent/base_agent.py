from app.ai.dependencies import AIDependencies, get_ai_dependencies
from app.ai.workflow.graph_config import create_security_rag_graph

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

class BaseAgent:
    def __init__(self, vector_store=None, deps=None):
        if deps is None:
            deps = get_ai_dependencies()
            
            if vector_store is not None:
                deps.vector_store = vector_store
                
        self.deps = deps
        
        self.memory = MemorySaver()

        graph = create_security_rag_graph(self.deps)
        self.graph = graph.compile(checkpointer=self.memory)

        self.state = None
        self.config = {
            "configurable": {
                "thread_id": "default_thread"
            }
        }

    def process_message(self, message: str) -> str:
        try:
            from app.ai.llm.llm import count_tokens
            
            if count_tokens(message) > self.deps.token_limit * 3:
                message = message[:4500]  
                print("Message truncated to ~1500 tokens for performance")

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