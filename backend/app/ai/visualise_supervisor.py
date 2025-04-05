# visualize_supervisor.py
from app.ai.workflow.graph_config import create_security_rag_graph
from app.ai.dependencies import initialize_dependencies
import os

def visualize_supervisor_workflow():
    """Generate a visualization of the supervisor-based workflow."""
    print("Initializing dependencies...")
    
    # Initialize AI dependencies
    deps = initialize_dependencies()
    
    # Create but don't run the graph
    print("Creating graph structure...")
    workflow = create_security_rag_graph(deps)
    
    # Generate Mermaid syntax
    print("Generating Mermaid diagram...")
    mermaid_syntax = workflow.get_graph().draw_mermaid()
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Save to file
    output_file = os.path.join(log_dir, "supervisor_workflow.mmd")
    with open(output_file, "w") as f:
        f.write(mermaid_syntax)
    
    print(f"Graph visualization saved to {output_file}")
    print("You can view this file in any Mermaid-compatible viewer or converter.")
    print("For example, paste the contents into https://mermaid.live")
    
    # Also print the syntax for convenience
    print("\nMermaid Syntax:")
    print(mermaid_syntax)

if __name__ == "__main__":
    visualize_supervisor_workflow()