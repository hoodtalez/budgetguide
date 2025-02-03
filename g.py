import requests
import openai

# Get AI-generated script
def generate_script(topic):
    api_key = "YOUR_OPENAI_API_KEY"
    prompt = f"Write a 5-minute YouTube script about {topic}."
    
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"model": "gpt-4", "prompt": prompt, "max_tokens": 400}

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    return response.json()["choices"][0]["text"]

topic = "Top 5 AI Tools to Make Money"
script = generate_script(topic)

# Save script
with open("script.txt", "w") as file:
    file.write(script)

print("Script Generated!")
