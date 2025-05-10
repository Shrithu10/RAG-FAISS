import faiss

# Load the index
index = faiss.read_index(r'C:\Users\Administrator 1\Desktop\techolution_rag\setup\lawyer_gpt_faiss.index')


# Check the number of vectors in the index
print("Vectors in FAISS index:", index.ntotal)
