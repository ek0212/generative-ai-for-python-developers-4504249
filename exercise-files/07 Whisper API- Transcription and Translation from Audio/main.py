# Import necessary libraries
import streamlit as st  # Streamlit for building the web application
import tempfile  # For creating temporary files
import openai  # OpenAI client library for accessing AI models
import os  # For handling environment variables
from dotenv import load_dotenv  # For loading environment variables from a .env file
from utils import speech_to_text, speech_to_translation, save_file  # Custom utility functions

# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key for authentication
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App setup
st.title("Audio transcriptions & translations")  # Add a title to the application

# Custom CSS styling for blue button
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

# User input section: form for uploading audio files
with st.form("user_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose a file")  # File upload input
    submit_button = st.form_submit_button(label="Submit")  # Submit button for the form

# Process the uploaded file when the user clicks the submit button
if submit_button and uploaded_file is not None:
    with st.spinner("Transcribing..."):  # Show a spinner while processing the file
        # Save the uploaded file to a temporary file location
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())  # Write the content of the uploaded file to the temp file
            temp_file_path = temp_file.name  # Get the path of the temporary file
            filename = temp_file_path.split("/")[-1]  # Extract the filename from the path

            # Transcribe the audio to text
            original_transcript = speech_to_text(temp_file_path)  # Get the transcription of the audio file

            # Translate the transcription into the target language
            translated_transcript = speech_to_translation(temp_file_path)  # Get the translated transcription

            # Save the original transcription to a file
            save_file(original_transcript, f"transcriptions/{uploaded_file.name}.txt")

            # Save the translated transcription to a file
            save_file(
                translated_transcript,
                f"transcriptions/{uploaded_file.name}_translated.txt",
            )

            # Display success message and transcription results
            st.success("File transcribed successfully!")  # Display success notification
            st.divider()  # Add a visual divider

            # Display the original transcript in blue text
            st.markdown(f":blue `{original_transcript}`")  

            st.divider()  # Add another visual divider

            # Display the translated transcript in green text
            st.markdown(f":green `{translated_transcript}`")  

            # Add an audio player to listen to the uploaded audio file
            st.audio(temp_file_path)  