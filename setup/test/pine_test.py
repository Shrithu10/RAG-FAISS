from pinecone import Pinecone

PINECONE_API_KEY = "pcsk_2FhJwo_BLN5kyXcVHymEv87MHdzsv9MJmCmwCAfKGx4TJ1zvTrdJok7Phcj3kwYM2pxfY9"
INDEX_NAME = "legal-data"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# ids = [str(i) for i in range(5)]  # Example: first 5 vectors
# response = index.fetch(ids=ids)

# print("=== FETCH BY ID ===")
# for vid, vdata in response.vectors.items():
#     print(f"ID: {vid}")
#     print(f"Metadata: {vdata.metadata}")
#     print(f"Embedding (first 5 dims): {vdata.values[:5]}")
#     print("-" * 40)

stats = index.describe_index_stats()
total_vectors = stats['total_vector_count']
print(f"Total vectors in index: {total_vectors}")


ids = [str(i) for i in range(5)]  # Check first 5 vectors
response = index.fetch(ids=ids)

# Print metadata keys and content for each fetched vector
for vid, vdata in response.vectors.items():
    print(f"ID: {vid}")
    print(f"Metadata keys: {list(vdata.metadata.keys())}")
    print(f"Metadata content: {vdata.metadata}")
    print("-" * 40)