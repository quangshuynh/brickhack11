from ollama import Client

# Initialize Ollama client with custom host
client = Client(host='http://129.21.42.90:11434')

def get_ollama_response(prompt: str) -> str:
    """
    Get a response from the Ollama model
    """
    try:
        response = client.chat(model='dolphin-llama3', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
