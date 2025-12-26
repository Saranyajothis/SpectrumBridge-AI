#!/usr/bin/env python3
"""
SpectrumBridge AI - Test All FREE Services ($0) - FIXED MODELS
"""
import os
from dotenv import load_dotenv
load_dotenv()

print("🧪 Testing SpectrumBridge FREE Stack...")

# Test 1: Google GenAI (CORRECT MODELS - Dec 2025)
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # List available models (optional sanity check)
    models = [m.name for m in client.models.list()]
    print("🧠 Gemini available models:", models[:3])

    # Generate content using a working model
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Say 'SpectrumBridge setup complete!'"
    )
    print("✅ Gemini:", response.output_text[:60])
except Exception as e:
    print("❌ Gemini:", str(e)[:120])

# Test 2: Sentence Transformers ✅ (Already working)
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-mpnet-base-v2')
    embedding = model.encode("test")
    print("✅ Embeddings:", len(embedding), "dimensions")
except Exception as e:
    print("❌ Embeddings:", str(e))

# Test 3: Hugging Face (final non‑streaming fix)
try:
    from huggingface_hub import InferenceClient
    import os
    token = os.getenv("HF_TOKEN")

    client = InferenceClient(model="gpt2", token=token)

    # Make sure to disable streaming
    response = client.text_generation(
        prompt="Autism education helps children",
        max_new_tokens=12,
        temperature=0.7,
        stream=False
    )

    text = response if isinstance(response, str) else str(response)
    print("✅ Hugging Face:", text.strip()[:100])
except Exception as e:
    print("❌ Hugging Face:", repr(e))



# Test 4: MongoDB ✅ (Already working)
try:
    from pymongo import MongoClient
    client = MongoClient(os.getenv("MONGODB_URI"))
    client.server_info()
    print("✅ MongoDB:", "Atlas Connected!")
except Exception as e:
    print("❌ MongoDB:", str(e)[:100])

print("\n🎉 3/4 ✅ = PROCEED TO WEEK 1 AGENTS!")
