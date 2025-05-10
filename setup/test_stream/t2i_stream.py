import streamlit as st
import sys

# Add the path to the t2i module
from t2i import query_stabilitydiff

st.title("💬 Text to Image")

# Ask the user for a prompt
prompt = st.text_input("Enter the description of the image you want to generate:")

# Check if the prompt is entered
if prompt:
    # Query the image generation function
    image = query_stabilitydiff(prompt)

    # Display the image
    st.image(image, caption=f"Image generated for: {prompt}", use_column_width=True)
