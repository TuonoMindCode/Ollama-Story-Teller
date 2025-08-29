import requests
import json

# Test with Qwen2.5 Instruct model - uses different prompt formatting
data = {
    "model": "huihui_ai/qwen2.5-abliterate:32b-instruct",
    "prompt": """<|im_start|>system
You are a creative storyteller who writes detailed, engaging narratives. Your stories should be comprehensive and well-developed, typically 3000-5000 words long. Include rich descriptions, character development, dialogue, and multiple scenes. Never rush to conclude your stories.
<|im_end|>
<|im_start|>user
Write a long, detailed fantasy story about a dragon and a brave knight. Include their first encounter, a conversation between them, the knight's backstory, the dragon's lair, and multiple scenes showing their relationship develop. Make this story substantial and detailed - at least 3000 words.
<|im_end|>
<|im_start|>assistant""",
    "options": {
        "num_predict": 8192,
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "stop": ["<|im_end|>"]  # Stop at end token for instruct models
    },
    "stream": True
}

print("Testing Qwen2.5-Abliterate Instruct Model")
print("=" * 50)
print("Sending to Ollama:")
print(json.dumps(data, indent=2))
print("\n" + "="*60)
print("STREAMING RESPONSE:")
print("="*60)

response = requests.post("http://localhost:11434/api/generate", json=data, stream=True)

full_response = ""
prompt_tokens = 0
response_tokens = 0
start_time = None

for line in response.iter_lines():
    if line:
        try:
            # Decode the line
            chunk = line.decode('utf-8')
            
            # Parse JSON
            chunk_data = json.loads(chunk)
            
            # Track timing
            if start_time is None:
                import time
                start_time = time.time()
            
            # Accumulate response text
            if 'response' in chunk_data:
                content = chunk_data['response']
                full_response += content
                print(content, end='', flush=True)  # Print as it streams
            
            # Check if done and get final metadata
            if chunk_data.get('done', False):
                import time
                end_time = time.time()
                generation_time = end_time - start_time if start_time else 0
                
                prompt_tokens = chunk_data.get('prompt_eval_count', 0)
                response_tokens = chunk_data.get('eval_count', 0)
                
                print(f"\n\n" + "="*60)
                print("STREAMING COMPLETED")
                print("="*60)
                break
                
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"\nError parsing chunk: {e}")
            continue

# Calculate performance metrics
words = len(full_response.split())
chars = len(full_response)
wpm = (words / generation_time * 60) if generation_time > 0 else 0
tokens_per_sec = response_tokens / generation_time if generation_time > 0 else 0

print(f"\nFINAL METADATA:")
print(f"Model: huihui_ai/qwen2.5-abliterate:32b-instruct")
print(f"Generation time: {generation_time:.2f} seconds")
print(f"Prompt tokens: {prompt_tokens}")
print(f"Response tokens: {response_tokens}")
print(f"Characters: {chars}")
print(f"Words: {words}")
print(f"Words per minute: {wpm:.0f}")
print(f"Tokens per second: {tokens_per_sec:.1f}")
print(f"Expected max tokens: 8192")
print(f"Actual vs Expected: {response_tokens}/8192 = {(response_tokens/8192)*100:.1f}%")

# Analyze results
if response_tokens < 3000:
    print(f"⚠️  WARNING: Response shorter than expected!")
    print(f"   Model stopped at {response_tokens} tokens")
    print(f"   This suggests natural story ending or model behavior")
elif response_tokens > 6000:
    print(f"✅ EXCELLENT: Model used {response_tokens} tokens (good length!)")
    print(f"   This model appears better at generating longer content")
else:
    print(f"✅ GOOD: Model used {response_tokens} tokens (decent length)")
    print(f"   Better than the previous model's ~1000 tokens")

# Check story quality indicators
if "dialogue" in full_response.lower() or '"' in full_response:
    print(f"✅ Story includes dialogue")
if len(full_response.split('\n\n')) > 3:
    print(f"✅ Story has multiple paragraphs/scenes")
if words > 2000:
    print(f"✅ Story is substantial length ({words} words)")
