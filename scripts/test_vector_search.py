"""
Test Vector Search
Interactive tool to test vector search queries against your autism knowledge base
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "spectrum_bridge_AI"
COLLECTION_NAME = "knowledge"
INDEX_NAME = "vector_index"

# Model
MODEL_NAME = "all-MiniLM-L6-v2"

class VectorSearchTester:
    def __init__(self):
        """Initialize MongoDB connection and embedding model"""
        print("Initializing...")
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        self.model = SentenceTransformer(MODEL_NAME)
        print("✓ Ready!\n")
    
    def search(self, query_text: str, limit: int = 5):
        """Perform vector search"""
        # Generate query embedding
        query_embedding = self.model.encode(query_text).tolist()
        
        # Vector search pipeline
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
        
        return list(self.collection.aggregate(pipeline))
    
    def display_results(self, results):
        """Display search results in a readable format"""
        if not results:
            print("\n⚠ No results found\n")
            return
        
        print(f"\n{'='*70}")
        print(f"Found {len(results)} results:")
        print(f"{'='*70}\n")
        
        for i, result in enumerate(results, 1):
            score = result.get('score', 0)
            source = result['metadata']['source']
            text = result['text']
            
            print(f"{i}. [{source}] (Score: {score:.4f})")
            print(f"   {text[:200]}...")
            if len(text) > 200:
                print(f"   [... {len(text)-200} more characters]")
            print()
    
    def interactive_search(self):
        """Interactive search mode"""
        print(f"{'='*70}")
        print("VECTOR SEARCH - INTERACTIVE MODE")
        print(f"{'='*70}\n")
        print("Enter your queries to search the autism knowledge base.")
        print("Commands:")
        print("  'quit' or 'exit' - Exit the program")
        print("  'stats' - Show database statistics")
        print(f"{'='*70}\n")
        
        while True:
            try:
                query = input("Query: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit']:
                    print("\nGoodbye!\n")
                    break
                
                if query.lower() == 'stats':
                    self.show_stats()
                    continue
                
                # Perform search
                results = self.search(query)
                self.display_results(results)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                break
            except Exception as e:
                print(f"\n✗ Error: {str(e)}\n")
    
    def show_stats(self):
        """Show database statistics"""
        total = self.collection.count_documents({})
        
        # Count unique sources
        pipeline = [
            {"$group": {"_id": "$metadata.source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        sources = list(self.collection.aggregate(pipeline))
        
        print(f"\n{'='*70}")
        print("DATABASE STATISTICS")
        print(f"{'='*70}")
        print(f"\nTotal documents: {total}")
        print(f"Unique PDFs: {len(sources)}")
        print(f"\nTop 10 sources by chunk count:")
        for source in sources[:10]:
            print(f"  • {source['_id']}: {source['count']} chunks")
        print(f"{'='*70}\n")
    
    def run_sample_queries(self):
        """Run sample queries"""
        sample_queries = [
            "What are the early signs of autism in children?",
            "How is autism diagnosed?",
            "What interventions are effective for autism?",
            "Tell me about sensory processing in autism",
            "What is Applied Behavior Analysis?",
        ]
        
        print(f"\n{'='*70}")
        print("SAMPLE QUERIES")
        print(f"{'='*70}\n")
        
        for query in sample_queries:
            print(f"\n{'='*70}")
            print(f"Query: {query}")
            print(f"{'='*70}")
            
            results = self.search(query, limit=3)
            self.display_results(results)
            
            input("\nPress Enter for next query...")

def main():
    print("\n" + "="*70)
    print("VECTOR SEARCH TESTER")
    print("="*70 + "\n")
    
    tester = VectorSearchTester()
    
    print("What would you like to do?")
    print("1. Interactive search")
    print("2. Run sample queries")
    print("3. Show statistics")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        tester.interactive_search()
    elif choice == "2":
        tester.run_sample_queries()
    elif choice == "3":
        tester.show_stats()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
