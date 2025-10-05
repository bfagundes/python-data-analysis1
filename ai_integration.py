from openai_module import generate_response

def ask_ai(prompt: str) -> str:
    """
    Generic wrapper to call the active AI provider.
    For now, it delegates to OpenAI. In the future,
    swap out the import with another provider.
    """
    try:
        return generate_response(prompt)
    except Exception as e:
        return "Failed to generate the response. Exception code: {e}"