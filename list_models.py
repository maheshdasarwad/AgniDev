import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve your API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in your .env file.")

# Configure the generative AI client with your API key
genai.configure(api_key=api_key)

# List all available models
models = genai.list_models()

# Print the list of models
print("Available Models:")
for model in models:
    print(model)
