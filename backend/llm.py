from ollama import Client
from typing import List, Dict

# Initialize Ollama client with custom host
client = Client(host='http://129.21.42.90:11434')

def get_ollama_response(prompt: str, history: List[Dict[str, str]] = None) -> str:
    """
    Get a response from the Ollama model
    
    Args:
        prompt: The current user message
        history: List of previous messages in the format [{"role": "user/assistant", "content": "message"}]
    
    Returns:
        str: The model's response
    """
    try:
        # Initialize history if None
        messages = history.copy() if history else []
        
        # Add current prompt
        messages.append({'role': 'user', 'content': prompt})
        
        # Get response from model
        response = client.chat(model='dolphin-llama3', messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
