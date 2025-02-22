from ollama import Client

# Initialize Ollama client with custom host
client = Client(host='http://localhost:11434')

def get_ollama_response(prompt: str) -> str:
    """
    Get a response from the Ollama model
    """
    try:
        response = client.chat(model='llama2', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
