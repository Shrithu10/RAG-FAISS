import streamlit as st
import faiss
import pinecone
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from google import genai
import torch
from pinecone import Pinecone, ServerlessSpec

# Configurations  
PINECONE_API_KEY = ""
PINECONE_ENVIRONMENT = "us-east-1"
INDEX_NAME = "legal-data"
INDEX_FILE = r"C:\Users\Administrator 1\Desktop\techolution_rag\setup\lawyer_gpt_faiss.index"
METADATA_FILE = r"C:\Users\Administrator 1\Desktop\techolution_rag\setup\lawyer_gpt_metadata.pkl"

#METADATA_FILE = "C:\Users\Administrator 1\Desktop\techolution_rag\setup\lawyer_gpt_metadata.pkl"
GEMINI_API_KEY = ""  # Replace with your actual Gemini API key
EMBEDDING_DIM = 384
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load FAISS index  
faiss_index = faiss.read_index(INDEX_FILE)  
with open(METADATA_FILE, "rb") as f:  
    faiss_metadata = pickle.load(f)

# Pinecone setup  
# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)  
# pinecone_index = pinecone.Index(INDEX_NAME)  
pc = Pinecone(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT
)
# Example of checking and creating an index
index_name = "lawyer-gpt"
existing_indexes = [index.name for index in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
    )
# Use the index
pinecone_index = pc.Index(index_name)
# Load embedding model  
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Gemini API client
client = genai.Client(api_key=GEMINI_API_KEY)

# Streamlit app layout  
st.title("Legal AI Assistant")  
query = st.text_input("Enter your legal question:")

# Define a prompt template
prompt_template = """
You are a legal assistant AI that provides legal advice based on a combination of legal context and a user's query.

Here is the context retrieved:
{context}

The user has asked the following question:
Q: {query}

Please provide a detailed and helpful response:
A:
"""

if query:  
    # Get embedding for the query  
    query_vector = embedding_model.encode(query).astype('float32')  

    # 1. Search Pinecone for context  
    #pinecone_results = pinecone_index.query(query_vector.tolist(), top_k=2, include_metadata=True)  
    pinecone_results = pinecone_index.query(
    vector=query_vector.tolist(),
    top_k=2,
    include_metadata=True
)

    pinecone_context = "\n".join([res["metadata"]["Instruction"] + " " + res["metadata"]["Response"] for res in pinecone_results["matches"]])  

    # 2. Search FAISS using cosine similarity  
    D, I = faiss_index.search(query_vector.reshape(1, -1), k=2)  
    faiss_context = "\n".join([faiss_metadata[idx]["question"] + " " + faiss_metadata[idx]["answer"] for idx in I[0]])

    # Combine contexts from Pinecone and FAISS
    full_context = (pinecone_context + "\n" + faiss_context).strip()  
    st.subheader("Retrieved Context:")  
    st.write(full_context)  

    # Generate the prompt using the template
    prompt = prompt_template.format(context=full_context, query=query)

    # 3. Generate response with Gemini API using the structured prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # Replace with the appropriate Gemini model name if needed
        contents=[prompt]
    )

    st.subheader("AI Response:")  
    st.write(response.text)