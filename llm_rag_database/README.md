
## Setup

1. Clone the repository

2. Create and activate a virtual environment:

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables by copying `.env.example` to `.env`:
```bash
cp .env.example .env
```

5. Configure your `.env` file:

## Usage

1. Place your PDF documents in the `data` directory:
```bash
mkdir data
# Copy your PDFs into the data directory
```

2. Ingest the PDFs to create the vector database:
```bash
python ingest_pdfs.py
```

3. Run the RAG application:
```bash
python llm_rag_database.py
```

This will launch a Gradio web interface where you can ask questions about your documents.

### Note
Unless you pay for hugging face premium good luck finding a model to run from there

