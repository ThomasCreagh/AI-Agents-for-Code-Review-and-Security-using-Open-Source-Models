# visualize_graph.py
from app.ai.workflow.graph_config import create_security_rag_graph
from app.ai.llm.llm import initialise_llm
from app.ai.database.init_chroma import initialize_vector_store

def visualize_workflow():
    """Generate a visualization of the security RAG workflow."""
    print("Initializing minimal components for visualization...")
    
    # Initialize components with minimal setup
    llm = initialise_llm()
    vector_store = initialize_vector_store()
    
    # Create but don't run the graph
    print("Creating graph structure...")
    workflow = create_security_rag_graph(llm, vector_store)
    
    # Generate Mermaid syntax
    print("Generating Mermaid diagram...")
    mermaid_syntax = workflow.get_graph().draw_mermaid()
    
    # Save to file
    output_file = "security_rag_graph.mmd"
    with open(output_file, "w") as f:
        f.write(mermaid_syntax)
    
    print(f"Graph visualization saved to {output_file}")
    print("You can view this file in any Mermaid-compatible viewer or converter.")
    print("For example, paste the contents into https://mermaid.live")
    
    # Also print the syntax for convenience
    print("\nMermaid Syntax:")
    print(mermaid_syntax)

if __name__ == "__main__":
    visualize_workflow()