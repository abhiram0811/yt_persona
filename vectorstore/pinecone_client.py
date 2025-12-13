# Vector store module - Embeddings and Pinecone
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "parkervectordb"

index = pc.Index(index_name)


def upsert_chunk(chunk_id: str, text: str, metadata: dict):
    index.upsert(vector)
