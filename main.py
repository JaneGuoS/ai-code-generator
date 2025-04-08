import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai
from pages import imageBase 

# Configure the API key directly in the script
API_KEY = 'AIzaSyCpLMWak0THJIeAduww7fZM0SePiqTgt2Y'
genai.configure(api_key=API_KEY)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Model name
MODEL_NAME = "AI Code Generator"

# Framework selection (e.g., Tailwind, Bootstrap, etc.)
framework = "Regular CSS use flex grid etc"  # Change this to "Bootstrap" or any other framework as needed

# Create the model
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Function to send a message to the model
def send_message_to_model(message, image_path):
    image_input = {
        'mime_type': 'image/jpeg',
        'data': pathlib.Path(image_path).read_bytes()
    }
    response = chat_session.send_message([message, image_input])
    return response.text

# Streamlit app
def main():
     # Set page configuration
    st.set_page_config(page_title="AI Code Generator 🏠", initial_sidebar_state="expanded")

    # Sidebar navigation
    st.sidebar.page_link("main.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/imageBase.py", label="Image Base AI Code Generator", icon="1️⃣")
    st.sidebar.page_link("pages/textBase.py", label="Text Base AI Code Generator", icon="2️⃣")
    st.sidebar.page_link("http://www.google.com", label="Google", icon="🌎")

    st.title("AI Code Generator 🏠")
    st.write("Welcome to the AI Code Generator! You can use this app to generate code snippets based on text or images.")


if __name__ == "__main__":
    main()
