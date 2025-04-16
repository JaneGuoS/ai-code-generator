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
def send_message_to_model(user_prompt: str, language: str) -> dict:
    """
    Sends a message to the AI model to generate code based on the user's input.

    Args:
        user_prompt (str): The user's problem description.
        language (str): The programming language specified by the user.

    Returns:
        dict: A dictionary containing the generated code and its explanation.
    """
    # Generate the AI prompt using the user's input
    ai_prompt = generate_code_prompt(user_prompt, language)

    # Send the prompt to the chat session
    response = chat_session.send_message([ai_prompt])
    # Output the raw response to the console


    # Parse the response text into a dictionary
    try:
        result = response.text
        # Remove the ```json markers
        cleaned_json_string = result.strip("```json").strip() # type: ignore

        # Convert the cleaned JSON string to a dictionary
        result_dict = json.loads(cleaned_json_string)

        if isinstance(result_dict, dict) and "code" in result_dict and "explanation" in result_dict:
            return result_dict
        else:
            raise ValueError("Response does not contain the expected keys: 'code' and 'explanation'.")
    except Exception as e:
        raise ValueError(f"Failed to parse the response: {e}")

def generate_code_prompt(user_prompt: str, language: str) -> str:
    """
    Generates an AI prompt for code generation based on user input.

    Args:
        user_prompt (str): The user's problem description.
        language (str): The programming language specified by the user.

    Returns:
        str: A JSON-formatted string containing the AI prompt.
    """
    ai_prompt = f"""You are an AI code generator for an application that accepts a user's request and generates code to solve the user's problem in multiple programming languages.The user's request is:
    "{user_prompt}" using "{language}" programming language.
    Please ensure your result is a JSON object containing the "code" and "explanation" keys in the format stated below.
    {{
        "code": "<Generated code>",
        "explanation": "<Explanation of the code>"
    }}
    """
    return ai_prompt.strip()
    
# Streamlit app
def main():
    # Sidebar navigation
    st.sidebar.page_link("main.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/requirementChat.py", label="Solution Generator based on requirement", icon="💬")
    st.sidebar.page_link("pages/imageBase.py", label="Image Base AI Code Generator", icon="👨‍💻")
    st.sidebar.page_link("pages/textBase.py", label="Text Base AI Code Generator", icon="📖")
    st.sidebar.page_link("http://www.google.com", label="Google", icon="🌎")
    st.title("Text Base AI Code Generator 📖 ")

    try:
        # Get the prompt
        userPrompt = st.text_area("Input and Refine the user prompt")
        language = st.selectbox(
            "Select the programming language:",
            options=["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "Rust"],
            index=0  # Default to the first option ("Python")
        )


        #Get the codes queried by the prompt
        if st.button("Generate Code"):
            st.write("🧑‍💻 Generating code...")
            response = send_message_to_model(userPrompt, language)
            # Fetch the code and explanation from the response dictionary
            code = response["code"]
            explanation = response["explanation"]

            # Display the generated code and explanation
            st.subheader("Generated Code:")
            st.code(code, language=language)

            # st.subheader("Explanation:")
            st.write(explanation)

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
