# https://platform.openai.com/docs/guides/speech-to-text/quickstart
# https://github.com/openai/whisper
# Import necessary libraries
import streamlit as st  # Streamlit for creating web applications
import tempfile  # For creating temporary files
import openai  # OpenAI API client library for interacting with Whisper model
import os  # For environment variable handling
from dotenv import load_dotenv  # For loading environment variables from a .env file
from utils import speech_to_text  # Custom utility function for converting speech to text

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key for authentication
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App setup
st.title("Audio transcription")  # Set the title of the Streamlit application

# Custom CSS styling for the blue button
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: transparent;
            border: 1px solid #3498db;
            float: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# User input section: form to upload files
with st.form("user_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose a file")  # File upload field
    submit_button = st.form_submit_button(label="Submit")  # Submit button

# Process the uploaded file when the user clicks the submit button
if submit_button and uploaded_file is not None:
    with st.spinner("Transcribing..."):  # Display a spinner while processing
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())  # Write the uploaded file content to the temp file
            temp_file_path = temp_file.name  # Get the path of the temporary file
            transcript = speech_to_text(temp_file_path)  # Convert speech to text using a custom function
            st.success("File transcribed successfully!")  # Display success message
            st.divider()  # Add a visual divider on the screen
            st.markdown(f":blue[{transcript}]")  # Display the transcription in blue text
            st.audio(temp_file_path)  # Add an audio player for listening to the uploaded file