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
            # Add a longer throttling delay to prevent overload errors
            import time
            print("Adding safety delay to prevent overload errors...")
            time.sleep(2.0)  # Wait 2 seconds before processing to avoid API overload
            
            from app.ai.llm.llm import count_tokens
            
            if count_tokens(message) > self.deps.token_limit * 3:
                message = message[:4500]  
                print("Message truncated to ~1500 tokens for performance")

            if self.state is None:
                # For the initial state, add extra delay as it's most resource-intensive
                time.sleep(1.0)
                
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
            
            # Handle overload errors specifically
            if "overloaded" in str(e).lower() or "529" in str(e):
                print("API overload detected, returning friendly message")
                return "I'm currently experiencing high demand. Please try again in a few moments while I optimize resources."
            
            return f"Error processing message: {str(e)}"

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error processing message: {str(e)}")
            print(error_trace)
            return f"Error processing message: {str(e)}"