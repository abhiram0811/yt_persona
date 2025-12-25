from vectorstore.pinecone_client import upsert_chunk, query_vector


print("Testing upsert......")
upsert_chunk(
    chunk_id="002",
    text="This sis parker test sample data text",
    metadata={"video_id": "test_vid", "title": "sample vid", "start_time": 0.0},
)
print("Upsert done✅")

print("Testing query....")
results = query_vector("What are is halloween fashion", top_k=1)
print(f"Found {(results)} matches:")
for match in results.matches:
    print(f"  - ID: {match.id}")
    print(f"  - Score: {match.score:.4f}")
    print(f"  - Metadata: {match.metadata}\n")
