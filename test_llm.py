import litellm

response = litellm.completion(
    model="ollama/mistral",
    messages=[
        {"role": "user", "content": "Give me 3 tips for closing a sales deal."}
    ],
    api_base="http://localhost:11434",
    timeout=60
)

print("✅ LLM Response:\n", response["choices"][0]["message"]["content"])
