import requests
import io
from PIL import Image

def query_stabilitydiff(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": "Bearer "}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return Image.open(io.BytesIO(response.content))


# import streamlit as st
# import requests
# import io
# from PIL import Image

# def query_stabilitydiff(payload, headers):
#     API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.content

# st.title("💬 Text to Image")

# # Ask the user for a prompt
# prompt = st.text_input("Enter the description of the image you want to generate:")

# # Check if the prompt is entered
# if prompt:
#     if not "your_hugging_face_api_key_here":  # Check if API key is provided
#         st.info("Please add your Hugging Face Token to continue.")
#         st.stop()

#     # Replace with your actual Hugging Face API key
#     headers = {"Authorization": "Bearer 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"}
    
#     # Query Stable Diffusion
#     image_bytes = query_stabilitydiff({
#         "inputs": prompt,
#     }, headers)

#     # Return Image
#     image = Image.open(io.BytesIO(image_bytes))

#     # Display the image
#     st.image(image, caption=f"Image generated for: {prompt}", use_column_width=True)
