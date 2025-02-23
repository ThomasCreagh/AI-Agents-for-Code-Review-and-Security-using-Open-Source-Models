from app.agent.base_agent import BaseAgent
from app.database.init_chroma import initialize_vector_store
from app.doc_loader.web_doc_loader import load_pdfs_from_directory
from app.doc_loader.doc_chunker import process_and_store_documents
import os

def main():
    """Main function to run the security-focused RAG system."""
    print("Initializing multi-agent security system...")
    
    # Initialize vector store first
    vector_store = initialize_vector_store()
    
    # Load and store documents from local directory
    print("Loading documents from data directory...")
    docs = load_pdfs_from_directory("app/doc_loader/data")
    if docs:
        print("Processing and storing documents...")
        process_and_store_documents(vector_store, docs)
    else:
        print("No documents were loaded from the data directory.")
    
    # Initialize agent with pre-populated vector store
    agent = BaseAgent(vector_store=vector_store)
    
    # Start an interactive loop
    print("\nSecurity RAG System initialized. Type 'exit' to quit, 'visualize' to create a graph visualization.")
    
    while True:
        try:
            # Get user input
            query = input("\nYour security question: ")
            
            # Check if user wants to exit
            if query.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
                
            # Check if user wants to visualize the graph
            elif query.lower() in ['visualize', 'viz', 'graph']:
                print("Generating graph visualization...")
                
                # Get the compiled graph from the agent
                graph = agent.graph
                
                # Generate Mermaid syntax
                output_file = "security_rag_graph.mmd"
                mermaid_syntax = graph.get_graph().draw_mermaid()
                
                # Save to file
                with open(output_file, "w") as f:
                    f.write(mermaid_syntax)
                
                print(f"Graph visualization saved to {output_file}")
                print("You can view this file with a Mermaid-compatible viewer or at https://mermaid.live")
                
                continue
            
            # Process the query through the agent
            print("\nProcessing through security analysis workflow...")
            response = agent.process_message(query)
            
            # Display the response
            print(f"\nResponse: {response}")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("The system will continue running. Please try again.")

if __name__ == "__main__":
    main()