import numpy as np
from datasets import load_dataset
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss
import pickle

MODEL_NAME = 'all-MiniLM-L6-v2'
EMBEDDING_DIM = 384
INDEX_FILE = 'lawyer_gpt_faiss.index'
METADATA_FILE = 'lawyer_gpt_metadata.pkl'

# Load SentenceTransformer model
model = SentenceTransformer(MODEL_NAME)

# Load the dataset
dataset = load_dataset("nisaar/Lawyer_GPT_India")["train"]

embeddings = []
metadata = []

for data in tqdm(dataset, desc="Encoding"):
    question = data.get("question", "")
    answer = data.get("answer", "")
    text = f"Q: {question}\nA: {answer}"
    if not question.strip() and not answer.strip():
        continue
    emb = model.encode(text)
    embeddings.append(emb)
    # Store both question and answer for later retrieval
    metadata.append({
        "question": question[:1000],  # Truncate for safety
        "answer": answer[:1000]
    })

if not embeddings:
    print("No embeddings generated. Check your dataset and sampling.")
    exit()

embeddings = np.vstack(embeddings).astype('float32')

# Build FAISS index
index = faiss.IndexFlatL2(EMBEDDING_DIM)
index.add(embeddings)
faiss.write_index(index, INDEX_FILE)

# Save metadata
with open(METADATA_FILE, "wb") as f:
    pickle.dump(metadata, f)

print(f"FAISS index and metadata saved: {INDEX_FILE}, {METADATA_FILE}")
print(f"Total vectors indexed: {len(embeddings)}")
print(f"FAISS index dimension: {index.d}")
