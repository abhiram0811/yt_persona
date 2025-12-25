# Vector store module - Embeddings and Pinecone
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "parkervectordb"

index = pc.Index(index_name)


def upsert_chunk(chunk_id: str, text: str, metadata: dict):
    embeddings = pc.inference.embed(
        model="llama-text-embed-v2", inputs=[text], parameters={"input_type": "passage"}
    )

    vector_values = embeddings.data[0].values

    index.upsert(
        vectors=[{"id": chunk_id, "values": vector_values, "metadata": metadata}]
    )


def query_vector(query_text: str, top_k: int = 3):
    """Search for the most similar chunks and return them"""
    embeddings = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[query_text],
        parameters={"input_type": "query"},
    )

    results = index.query(
        vector=embeddings.data[0].values, top_k=top_k, include_metadata=True
    )
    return results
