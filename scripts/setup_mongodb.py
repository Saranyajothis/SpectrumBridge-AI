# scripts/setup_mongodb.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["spectrum_bridge_AI"]

# Create collections
db.create_collection("teaching_strategies")
db.create_collection("adapted_lessons")

# Vector index (YOUR plan exactly)
db["teaching_strategies"].create_index([
    {"embedding": "vector"},
    {
        "name": "vector_index",
        "numDimensions": 768,  # Sentence Transformers
        "similarity": "cosine"
    }
])
print("✅ MongoDB ready with vector index!")
