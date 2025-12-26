"""
Step 2: Download Embedding Model
Downloads sentence-transformers model for local embedding generation
"""

from sentence_transformers import SentenceTransformer
from pathlib import Path
import torch

# Model storage path
MODEL_DIR = Path(__file__).parent.parent / "knowledge_base" / "embeddings"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Using a high-quality model optimized for semantic search
MODEL_NAME = "all-MiniLM-L6-v2"  # 384 dimensions, fast and efficient
# Alternative models:
# "all-mpnet-base-v2"  # 768 dimensions, higher quality but slower
# "multi-qa-MiniLM-L6-cos-v1"  # Optimized for Q&A

def download_embedding_model(model_name=MODEL_NAME):
    """Download and cache the embedding model"""
    
    print(f"\n{'='*60}")
    print(f"Downloading Embedding Model: {model_name}")
    print(f"{'='*60}\n")
    
    try:
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {device}")
        
        # Download model (will cache automatically)
        print(f"Loading model from HuggingFace...")
        model = SentenceTransformer(model_name, device=device)
        
        # Test the model
        print(f"\nTesting model...")
        test_text = "Autism is a developmental disorder."
        embedding = model.encode(test_text)
        
        print(f"✓ Model loaded successfully!")
        print(f"✓ Embedding dimension: {len(embedding)}")
        print(f"✓ Device: {device}")
        
        # Get model info
        print(f"\n{'='*60}")
        print(f"Model Information:")
        print(f"{'='*60}")
        print(f"Name: {model_name}")
        print(f"Dimension: {model.get_sentence_embedding_dimension()}")
        print(f"Max Sequence Length: {model.max_seq_length}")
        print(f"{'='*60}\n")
        
        return model
        
    except Exception as e:
        print(f"✗ Error downloading model: {str(e)}")
        return None

def test_embedding_generation(model):
    """Test embedding generation with sample texts"""
    
    print(f"\n{'='*60}")
    print("Testing Embedding Generation")
    print(f"{'='*60}\n")
    
    test_texts = [
        "Children with autism may have difficulty with social communication.",
        "Early intervention can significantly improve outcomes for autistic children.",
        "Sensory processing differences are common in autism spectrum disorder.",
        "Applied Behavior Analysis (ABA) is a common therapeutic approach.",
    ]
    
    print("Generating embeddings for sample texts...")
    embeddings = model.encode(test_texts, show_progress_bar=True)
    
    print(f"\n✓ Generated {len(embeddings)} embeddings")
    print(f"✓ Each embedding shape: {embeddings[0].shape}")
    
    # Test similarity
    from numpy import dot
    from numpy.linalg import norm
    
    def cosine_similarity(a, b):
        return dot(a, b) / (norm(a) * norm(b))
    
    print(f"\n{'='*60}")
    print("Similarity Test:")
    print(f"{'='*60}")
    
    for i in range(len(test_texts)):
        for j in range(i+1, len(test_texts)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"\nText {i+1} vs Text {j+1}:")
            print(f"  Similarity: {sim:.4f}")
            if sim > 0.5:
                print(f"  → High similarity ✓")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("EMBEDDING MODEL DOWNLOAD")
    print("="*60)
    
    # Download model
    model = download_embedding_model()
    
    if model:
        # Test it
        test_embedding_generation(model)
        
        print("✓ Model ready for use!")
        print("\nNext Steps:")
        print("1. Model is cached and ready to use")
        print("2. Proceed to Step 3: Process PDFs and generate embeddings")
    else:
        print("✗ Model download failed. Please check your internet connection.")
