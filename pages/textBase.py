import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai

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
MODEL_NAME = "Text Base AI Code Generator"

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
def send_message_to_model(message):
    response = chat_session.send_message([message])
    return response.text

# Streamlit app
def main():
    st.title("Text Base AI Code Generator 👨‍💻 ")

    try:
        # Get the text description
        description = st.text_area("Input the description")

        # Refine the description
        st.write("🔍 Refining description with visual comparison...")
        refine_prompt = f"Compare the described UI elements with the provided image and identify any missing elements or inaccuracies. Also Describe the color of the elements. Provide a refined and accurate description of the UI elements based on this comparison. Here is the initial description: {description}"
        refined_description = send_message_to_model(refine_prompt)
        st.write(refined_description)

        # Generate HTML
        st.write("🛠️ Generating website...")
        html_prompt = f"Create an HTML file based on the following UI description, using the UI elements described in the previous response. Include {framework} CSS within the HTML file to style the elements. Make sure the colors used are the same as the original UI. The UI needs to be responsive and mobile-first, matching the original UI as closely as possible. Do not include any explanations or comments. Avoid using ```html. and ``` at the end. ONLY return the HTML code with inline CSS. Here is the refined description: {refined_description}"
        initial_html = send_message_to_model(html_prompt)
        st.code(initial_html, language='html')

        # Refine HTML
        st.write("🔧 Refining website...")
        refine_html_prompt = f"Validate the following HTML code based on the UI description and image and provide a refined version of the HTML code with {framework} CSS that improves accuracy, responsiveness, and adherence to the original design. ONLY return the refined HTML code with inline CSS. Avoid using ```html. and ``` at the end. Here is the initial HTML: {initial_html}"
        refined_html = send_message_to_model(refine_html_prompt)
        st.code(refined_html, language='html')

        # Save the refined HTML to a file
        with open("index.html", "w") as file:
            file.write(refined_html)
        st.success("HTML file 'index.html' has been created.")

        # Provide download link for HTML
        st.download_button(label="Download HTML", data=refined_html, file_name="index.html", mime="text/html")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
