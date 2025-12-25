from vectorstore.pinecone_client import index

stats = index.describe_index_stats()
print(f"Index Stats:\n{stats}")
