# https://platform.openai.com/docs/guides/text-generation/completions-api
# Import necessary libraries
import os  # For environment variable handling
import openai  # OpenAI's Python client library for API interaction
import tiktoken  # For token counting and encoding text
from colorama import Fore  # For colored terminal text
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load the environment variables from a .env file to set up the OpenAI API client
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Retrieve the API key from environment variables
client = openai.OpenAI()  # Initialize the OpenAI client

# Set up the language model and a test prompt
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"  # Define the model to use
PROMPT_TEST = "This is a test prompt. Say this is a test"  # Example prompt for testing purposes

def get_tokens(user_input: str) -> int:
    """
    Returns the number of tokens in a text string.
    
    Args:
        user_input (str): The text input for which token count is needed.
    
    Returns:
        int: The number of tokens in the provided text.
    """
    encoding = tiktoken.get_encoding("cl100k_base")  # Use a specific encoding method

    token_integers = encoding.encode(user_input)  # Encode the input text into token integers
    tokens_usage = len(token_integers)  # Count the number of tokens used

    # Decode each token integer into its string representation
    tokenized_input = list(
        map(
            lambda x: encoding.decode_single_token_bytes(x).decode("utf-8"),
            encoding.encode(user_input),
        )
    )
    # Display token usage details
    print(f"{encoding}: {tokens_usage} tokens")
    print(f"Token integers: {token_integers}")
    print(f"Token bytes: {tokenized_input}")

def start():
    """Display the main menu and prompt the user for input."""
    print("MENU")
    print("====")
    print("[1]- Ask a question")
    print("[2]- Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        ask()  # Proceed to ask a question
    elif choice == "2":
        exit()  # Exit the program
    else:
        print("Invalid choice")  # Handle invalid menu selections

def ask():
    """Prompt the user to ask a question and generate a response using the model."""
    instructions = (
        "Type your question and press ENTER. Type 'x' to go back to the MAIN menu.\n"
    )
    # Display instructions in blue italicized text
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)

    user_input = input("Q: ")  # Capture user input as a question

    # Loop to handle user interactions until they choose to exit
    while True:
        if user_input == "x":  # Return to the main menu if 'x' is pressed
            start()
        else:
            # Create a completion request using the selected language model
            completion = client.completions.create(
                model=LANGUAGE_MODEL,
                prompt=str(user_input)
            )
            response = completion['choices'][0]['text']  # Extract the response text from the API response
            get_tokens(response)  # Calculate and display token usage

            # Display the model's response in blue text
            print(Fore.BLUE + f"A: " + response + Fore.RESET)
            print(Fore.WHITE + "\n-------------------------------------------------")

# Entry point of the application
if __name__ == "__main__":
    start()