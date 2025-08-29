import requests
import json

# Test what Ollama actually receives
data = {
    "model": "dolphin-mixtral:8x7b-un8k",
    "prompt": "Write a very long story about a dragon.",
    "options": {
        "num_predict": 8192,
        "temperature": 0.8
    },
    "stream": True
}

print("Sending to Ollama:")
print(json.dumps(data, indent=2))
print("\n" + "="*60)
print("STREAMING RESPONSE:")
print("="*60)

response = requests.post("http://localhost:11434/api/generate", json=data, stream=True)

full_response = ""
prompt_tokens = 0
response_tokens = 0

for line in response.iter_lines():
    if line:
        try:
            # Decode the line
            chunk = line.decode('utf-8')
            
            # Parse JSON
            chunk_data = json.loads(chunk)
            
            # Accumulate response text
            if 'response' in chunk_data:
                content = chunk_data['response']
                full_response += content
                print(content, end='', flush=True)  # Print as it streams
            
            # Check if done and get final metadata
            if chunk_data.get('done', False):
                prompt_tokens = chunk_data.get('prompt_eval_count', 0)
                response_tokens = chunk_data.get('eval_count', 0)
                print(f"\n\n" + "="*60)
                print("STREAMING COMPLETED")
                print("="*60)
                break
                
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"\nError parsing chunk: {e}")
            continue

print(f"\nFINAL METADATA:")
print(f"Prompt tokens: {prompt_tokens}")
print(f"Response tokens: {response_tokens}")
print(f"Response length: {len(full_response)} characters")
print(f"Word count: {len(full_response.split())} words")
print(f"Expected tokens: 8192")
print(f"Actual vs Expected: {response_tokens}/8192 = {(response_tokens/8192)*100:.1f}%")

# Test if it stopped early
if response_tokens < 8000:  # Allow some margin
    print(f"⚠️  WARNING: Response much shorter than expected!")
    print(f"   This suggests the model stopped early, not due to token limits.")
else:
    print(f"✅ Good: Response used most of the available tokens.")
