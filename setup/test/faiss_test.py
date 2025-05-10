import faiss

# Load the index
index = faiss.read_index(r'faiss.index')


# Check the number of vectors in the index
print("Vectors in FAISS index:", index.ntotal)
