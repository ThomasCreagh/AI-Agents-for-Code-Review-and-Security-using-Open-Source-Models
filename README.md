# AI Agents for Code Review and Security

This repository contains a full-stack application that leverages AI agents to perform automated code review and security analysis. It uses a sophisticated, graph-based workflow built with LangGraph, allowing for intelligent routing and analysis based on user input. The system is designed to be flexible, supporting both local open-source models via Ollama and powerful cloud APIs like Anthropic's Claude.

## Key Features

-   **AI-Powered Code Analysis**: Utilizes AI agents to review code for security vulnerabilities, best practices, and potential bugs.
-   **LangGraph-Based Agentic Workflow**: A supervisor agent analyzes user queries and routes them to specialized agents for code analysis, static security scanning (`bandit`), or Retrieval-Augmented Generation (RAG).
-   **Retrieval-Augmented Generation (RAG)**: Enhance analysis by referencing a knowledge base of security documents. Upload your own PDF documents (e.g., OWASP, NIST standards) to create a custom security context.
-   **Hybrid LLM Support**: Natively supports local, open-source models via Ollama and can be easily configured to use Anthropic's Claude API for more powerful analysis.
-   **Full-Stack Application**: Comes with a responsive Next.js frontend and a robust FastAPI backend.
-   **Static & Dynamic Analysis**: Combines Abstract Syntax Tree (AST) analysis for understanding code structure with static analysis tools like `bandit` for identifying common security issues in Python.
-   **Containerized**: Fully containerized with Docker and Docker Compose for easy, cross-platform setup and deployment.
-   **CI/CD Integration**: Includes a `.gitlab-ci.yml` for automated testing and deployment pipelines.

## Architecture

The application is composed of several containerized services orchestrated by `docker-compose`:

-   **`frontend`**: A Next.js web application that provides the user interface for uploading code, managing security documents, and viewing analysis results.
-   **`backend`**: A Python FastAPI server that exposes a REST API for handling analysis requests and managing the AI workflow.
-   **`ollama`**: A service that runs and serves open-source Large Language Models locally, providing inference capabilities for the AI agents.
-   **`reverse-proxy` (Deployment)**: A Traefik reverse proxy is used in the deployment configuration (`docker-compose-deploy.yml`) to manage traffic and handle SSL termination.

The backend uses a ChromaDB vector store (persisted to the local filesystem) to store embeddings of uploaded security documents, enabling the RAG functionality.

## AI Agent Workflow

The core of the application is a multi-agent system built with LangGraph. The workflow is orchestrated as follows:

1.  **Supervisor Agent**: Receives the initial user query (which includes the code to be analyzed). It determines the nature of the request and decides the next step.
2.  **Routing**: Based on the query content, the supervisor routes the task to one of the following paths:
    -   **Code Analysis Path**: If the query contains code.
    -   **Security Question Path**: If the query is about security concepts without code.
    -   **General RAG Path**: For general queries requiring information retrieval.
3.  **Code Analysis (`ast_node`)**: If code is present, this node performs an Abstract Syntax Tree (AST) analysis to extract function definitions, parameters, and other structural information.
4.  **Bandit Scan (`bandit_node`)**: The extracted Python code is passed to the `bandit` tool for a static security scan. The results are added to the context.
5.  **RAG (`rag_node`)**: The agent uses the query and the context from the code analysis to retrieve relevant chunks from the security documents stored in the ChromaDB vector store.
6.  **Integration (`integrated_node`)**: This node synthesizes the information gathered from the AST analysis, bandit scan, and retrieved documents into a consolidated context for the final analysis.
7.  **Security Analysis (`security_node`)**: A specialized agent performs a detailed security review using the integrated context, focusing on vulnerabilities and best practices.
8.  **Response Generation (`response_node`)**: The final agent compiles all the analysis and findings into a structured, human-readable markdown response.

## Getting Started

### Prerequisites

-   Docker
-   Docker Compose

### Installation and Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ThomasCreagh/AI-Agents-for-Code-Review-and-Security-using-Open-Source-Models.git
    cd AI-Agents-for-Code-Review-and-Security-using-Open-Source-Models
    ```

2.  **Create an environment file:**
    Copy the example environment file to create your own configuration.
    ```sh
    cp .env.example .env
    ```
    Open the `.env` file and configure the variables. At a minimum, you should set:
    ```env
    # A simple key for securing the API between frontend and backend
    NEXT_PUBLIC_API_KEY=your-secret-key-here

    # The URL for the backend API
    NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/api/v1

    # To use Anthropic's Claude instead of a local model
    # USE_ANTHROPIC=true
    # ANTHROPIC_API_KEY=your-anthropic-api-key
    ```
    For GPU acceleration with Ollama, ensure your NVIDIA drivers are installed and configure `OLLAMA_GPU_LAYERS` in the `.env` file.

3.  **Build and run the application with Docker Compose:**
    This command will build the Docker images for the frontend, backend, and Ollama services and start them. The first run will also download the default LLMs (`granite3.1-dense:2b` and `nomic-embed-text`), which may take some time.

    ```sh
    docker compose up --build -d
    ```

4.  **Access the application:**
    -   Frontend UI: [http://localhost:3000](http://localhost:3000)
    -   Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Usage

Once the application is running, you can use it via the web interface:

1.  **Navigate to the Security Analysis page** (`/security-analysis`).
2.  **(Optional) Manage Documents**:
    -   Upload your own PDF security documents to the knowledge base. This will allow the RAG agent to use them for context during analysis.
    -   You can view database statistics or clear all uploaded documents from this page.
3.  **Analyze Code**:
    -   Upload a code file you wish to analyze.
    -   Select the programming language.
    -   Optionally, provide a security focus or specific question in the text area.
    -   If you have uploaded documents, check the "Reference security documentation" box to enable the RAG system.
    -   Click "Analyze Code" to submit the request.
4.  **View Results**: The analysis results will be displayed in markdown format on the page.

### Key API Endpoints

You can also interact with the backend API directly.

-   `POST /api/v1/ast-analysis/submit-code-for-review`: The primary endpoint for submitting a code file for a full security review.
-   `POST /api/v1/documents/upload`: Upload a PDF document to the RAG knowledge base.
-   `POST /api/v1/database/clear`: Clears all documents from the vector store.
-   `GET /api/v1/database/stats`: Retrieves statistics about the vector store, such as the number of documents.
-   `GET /api/v1/graph`: Returns a Mermaid syntax representation of the LangGraph workflow.
