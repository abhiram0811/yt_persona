# ParkerStyle Advisor

A fashion & lifestyle AI assistant powered by RAG, inspired by Parker York Smith's content.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
pytest --cov  # with coverage
```

## Project Structure

```
ingestion/      # YouTube API client, fetch videos/transcripts
processing/     # Cleaning, chunking, metadata enrichment
vectorstore/    # Pinecone client, embeddings, upsert
api/            # FastAPI backend
ui/next-app/    # Next.js frontend
tests/          # pytest test suite
```
