from pinecone import Pinecone, ServerlessSpec
from datasets import load_dataset
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Config
PINECONE_API_KEY = ""
PINECONE_ENVIRONMENT = "us-east-1"
INDEX_NAME = "legal-data"
EMBEDDING_DIM = 384

# Pinecone setup
pc = Pinecone(api_key=PINECONE_API_KEY)

# Delete the old index if it exists (to avoid dimension mismatch)
if INDEX_NAME in pc.list_indexes().names():
    print(f"Deleting old index '{INDEX_NAME}' (wrong dimension)...")
    pc.delete_index(INDEX_NAME)

# Now create the new index with the correct dimension
pc.create_index(
    name=INDEX_NAME,
    dimension=EMBEDDING_DIM,  # 384 for all-MiniLM-L6-v2
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
)
index = pc.Index(INDEX_NAME)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load dataset
dataset = load_dataset("viber1/indian-law-dataset")

vectors = []
batch_size = 100
MAX_METADATA_CHARS = 10000  # ~10 KB for each field, well under 40KB total

for i, data in enumerate(tqdm(dataset["train"])):
    instruction = data.get("Instruction", "")
    response = data.get("Response", "")
    # Combine for embedding
    text = (instruction + " " + response).strip()
    if not text:
        continue
    # Truncate to avoid exceeding 40KB metadata limit
    meta_instruction = instruction[:MAX_METADATA_CHARS]
    meta_response = response[:MAX_METADATA_CHARS]

    vector = model.encode(text)
    vectors.append(
        (
            str(i),
            vector.tolist(),
            {"Instruction": meta_instruction, "Response": meta_response}
        )
    )
    if len(vectors) >= batch_size:
        index.upsert(vectors)
        vectors = []

if vectors:
    index.upsert(vectors)

print("Indexing completed!")
