"""
Simple RAG Query Interface
Combines vector search with LLM generation for question answering
Using Groq API for fast, free LLM inference
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load environment variables
load_dotenv()

# Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_NAME = "spectrum_bridge_AI"
COLLECTION_NAME = "knowledge"
INDEX_NAME = "vector_index"
MODEL_NAME = "all-MiniLM-L6-v2"

class SimpleRAG:
    def __init__(self):
        """Initialize RAG system"""
        print("Initializing RAG system...")
        
        # MongoDB connection
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        
        # Embedding model
        self.embedding_model = SentenceTransformer(MODEL_NAME)
        
        # Groq LLM
        self.llm = Groq(api_key=GROQ_API_KEY)
        
        print("✓ RAG system ready!\n")
    
    def retrieve_context(self, query: str, limit: int = 5) -> str:
        """Retrieve relevant context from vector database"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Vector search
        pipeline = [
            {
                "$vectorSearch": {
                    "index": INDEX_NAME,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 50,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        # Combine retrieved texts
        context_parts = []
        sources = []
        
        for result in results:
            context_parts.append(result['text'])
            sources.append({
                'source': result['metadata']['source'],
                'score': result.get('score', 0)
            })
        
        context = "\n\n".join(context_parts)
        return context, sources
    
    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using Groq LLM with retrieved context"""
        
        prompt = f"""You are an expert assistant on autism spectrum disorder (ASD). 
Answer the following question based ONLY on the provided context from research documents.
If the context doesn't contain enough information to answer the question, say so.

Context from research documents:
{context}

Question: {query}

Provide a clear, accurate, and helpful answer based on the context above. 
If you cite specific information, mention it comes from the research documents."""

        try:
            chat_completion = self.llm.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert assistant on autism spectrum disorder. Provide accurate, helpful answers based on research documents."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",  # Updated model - Fast and high quality
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def query(self, question: str, show_sources: bool = True):
        """Complete RAG query: retrieve + generate"""
        print(f"\n{'='*70}")
        print(f"Question: {question}")
        print(f"{'='*70}\n")
        
        # Retrieve context
        print("🔍 Searching knowledge base...")
        context, sources = self.retrieve_context(question)
        
        if not context:
            print("⚠ No relevant information found in knowledge base\n")
            return
        
        print(f"✓ Found {len(sources)} relevant documents\n")
        
        # Generate answer
        print("🤖 Generating answer with Groq...\n")
        answer = self.generate_answer(question, context)
        
        # Display answer
        print(f"{'='*70}")
        print("ANSWER:")
        print(f"{'='*70}\n")
        print(answer)
        print()
        
        # Display sources
        if show_sources:
            print(f"{'='*70}")
            print("SOURCES:")
            print(f"{'='*70}\n")
            for i, source in enumerate(sources, 1):
                print(f"{i}. {source['source']} (relevance: {source['score']:.4f})")
            print()
    
    def interactive_mode(self):
        """Interactive Q&A mode"""
        print(f"{'='*70}")
        print("INTERACTIVE RAG MODE (Powered by Groq)")
        print(f"{'='*70}\n")
        print("Ask questions about autism. Type 'quit' to exit.\n")
        
        while True:
            try:
                question = input("Your question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye!\n")
                    break
                
                self.query(question)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                break
            except Exception as e:
                print(f"\n✗ Error: {str(e)}\n")

def main():
    print("\n" + "="*70)
    print("AUTISM RAG SYSTEM - Q&A INTERFACE (Groq Powered)")
    print("="*70 + "\n")
    
    # Initialize RAG
    rag = SimpleRAG()
    
    # Ask if user wants to try sample questions or interactive mode
    print("Choose mode:")
    print("1. Interactive mode (ask your own questions)")
    print("2. Run sample questions")
    print()
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        rag.interactive_mode()
    elif choice == "2":
        sample_questions = [
            "What are the early signs of autism in children?",
            "How is autism spectrum disorder diagnosed?",
            "What are effective interventions for autism?",
            "Tell me about sensory processing issues in autism",
            "What is Applied Behavior Analysis therapy?"
        ]
        
        for question in sample_questions:
            rag.query(question)
            input("\nPress Enter for next question...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
