import requests
import json

# Test what Ollama actually receives (non-streaming)
data = {
    "model": "dolphin-mixtral:8x7b-un8k",
    "prompt": "Write a very long story about a dragon. Make it detailed and extensive with rich descriptions, character development, and multiple scenes. Do not rush to conclude the story.",
    "options": {
        "num_predict": 8192,
        "temperature": 0.8,
        "stop": []  # No stop tokens
    },
    "stream": False
}

print("Sending to Ollama:")
print(json.dumps(data, indent=2))
print("\nGenerating (this may take a few minutes)...")

response = requests.post("http://localhost:11434/api/generate", json=data)
result = response.json()

print(f"\nResponse metadata:")
print(f"Prompt tokens: {result.get('prompt_eval_count', 'unknown')}")
print(f"Response tokens: {result.get('eval_count', 'unknown')}")
print(f"Response length: {len(result.get('response', ''))} characters")
print(f"Word count: {len(result.get('response', '').split())} words")

response_tokens = result.get('eval_count', 0)
if response_tokens < 8000:
    print(f"⚠️  Model stopped at {response_tokens} tokens (much less than 8192 limit)")
    print("This suggests natural story ending, not token limit reached")
else:
    print(f"✅ Model used {response_tokens} tokens (close to 8192 limit)")

# Show first 500 characters of response
response_text = result.get('response', '')
print(f"\nFirst 500 characters of response:")
print("-" * 50)
print(response_text[:500])
print("..." if len(response_text) > 500 else "")
