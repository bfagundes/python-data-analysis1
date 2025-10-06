import os
from openai import OpenAI
from config_api import OPENAI_API_KEY

# Create client safely (uses env var for API key)
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Sends a prompt to OpenAI API and returns the text response.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()