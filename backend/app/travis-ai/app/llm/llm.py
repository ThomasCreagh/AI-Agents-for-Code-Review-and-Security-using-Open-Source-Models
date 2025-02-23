from langchain_ollama import ChatOllama 

def initialise_llm(model: str = "granite3.1-dense:2b") -> ChatOllama:
    print(f"LLM Model: {model}")
    llm = ChatOllama(
        base_url="http://localhost:11434",
        model=model,
        temperature=0
    ) 
    return llm