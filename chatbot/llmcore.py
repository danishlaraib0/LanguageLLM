import requests

def ollama_generate(system_prompt, context, user_query):
    # Combining system prompt, context, and user query into one prompt
    combined_prompt = f"System: {system_prompt}\nContext: {context}\nUser: {user_query}\n"
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi4",
            "prompt": combined_prompt,
            "stream": False
        }
    )
    return response.json().get('response', '')


system_prompt = "You are an AI assistant helping with language learning and you have to give response in json with key response and weaktopic(if topic is weak then give here else none)."
context = "i am danish i want to learn english and my level is easy."
user_query = "What is the capital of Japan?"

response = ollama_generate(system_prompt, context, user_query)
print(response)
