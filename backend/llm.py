from ollama import Client

# Initialize Ollama client with custom host
client = Client(host='http://129.21.42.90:11434')

def get_ollama_response(prompt: str, history=[]) -> str:
    """
    Get a response from the Ollama model
    """
    try:
        message = {'role': 'user', 'content': prompt}
        history.append(message)
        response = client.chat(model='dolphin-llama3', messages=history)
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
