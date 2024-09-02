# Import necessary libraries and modules
import os
from dotenv import load_dotenv  # To load environment variables from a .env file
from langchain.chat_models import ChatOpenAI  # To use OpenAI's chat models
from langchain.prompts import ChatPromptTemplate  # To create a structured prompt for the chat model

# Import classes for creating prompt templates
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,  # Template for messages from a human user
    SystemMessagePromptTemplate,  # Template for system messages (assistant role)
)
from langchain.schema import StrOutputParser  # To parse the output of the chat model as a string

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the language model to be used
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"

# Define the system prompt that sets the assistant's role
system_prompt = "You are a helpful assistant that answers general inquiries and assists with technical issues."

# Initialize a string output parser
str_parser = StrOutputParser()

# Initialize the chat model with specific settings
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

# Create system and human message prompts using templates
system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")

# Combine the system and human prompts into a chat prompt template
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

def main():
    # Example user input
    user_input = "I want to return a pair of shoes"

    # Generate the prompt value by invoking the chat prompt with the user's question
    prompt_value = chat_prompt.invoke({"question": user_input})

    # Format the chat prompt to messages compatible with the model
    messages = chat_prompt.format_prompt(question=user_input).to_messages()

    # Generate the response from the chat model using the formatted messages
    response = model.invoke(messages)
    print(response)  # Print the model's raw response

    # Parse the response content as a string
    content = str_parser.invoke(response)
    print(content)  # Print the parsed string content

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
