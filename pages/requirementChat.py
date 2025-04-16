import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai
import json

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
MODEL_NAME = "gemini-1.5-pro-latest"

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
# Function to send a message to the model
def send_message_to_model(message):
    response = chat_session.send_message(message)
    return response.text

# Streamlit app
def main():
    # Sidebar navigation
    st.sidebar.page_link("main.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/requirementChat.py", label="Solution Generator based on requirement", icon="💬")
    st.sidebar.page_link("pages/imageBase.py", label="Image Base AI Code Generator", icon="👨‍💻")
    st.sidebar.page_link("pages/textBase.py", label="Text Base AI Code Generator", icon="📖")
    st.sidebar.page_link("http://www.google.com", label="Google", icon="🌎")
    st.title("Solution Generator 💬 ")

    try:
        response = None
        # Get the prompt
        userPrompt = st.text_area("Input the requirement")

        #Get the codes queried by the prompt
        if st.button("Generate Solution"):
            st.write("🧑‍💻 Generating Solution...")
            if response:
               refine_prompt = f"Refine the solution based om the user prompt: {userPrompt} and based on previous response: {response}"
               response = send_message_to_model(refine_prompt)
            else:
              response = send_message_to_model(userPrompt)

            st.subheader("Generated Solution:")
            st.text(response)

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
