"""
RAG System with Content Adapter Integration
Combines vector search with Gemini-powered content simplification
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import sys

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.content_adapter import ContentAdapter

# Load environment variables
load_dotenv()

# Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_NAME = "spectrum_bridge_AI"
COLLECTION_NAME = "knowledge_base"
INDEX_NAME = "vector_index"
MODEL_NAME = "all-MiniLM-L6-v2"


class AdaptiveRAG:
    """
    RAG system that retrieves information and adapts it to Grade 2 reading level
    """
    
    def __init__(self):
        """Initialize RAG system with vector search and content adapter"""
        print("Initializing Adaptive RAG System...")
        
        # MongoDB connection
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        
        # Embedding model for search
        self.embedding_model = SentenceTransformer(MODEL_NAME)
        
        # Gemini LLM
        genai.configure(api_key=GEMINI_API_KEY)
        self.llm = genai.GenerativeModel('gemini-pro')
        
        # Content Adapter
        self.adapter = ContentAdapter()
        
        print("✓ Adaptive RAG System ready!\n")
    
    def retrieve_context(self, query: str, limit: int = 5) -> tuple:
        """
        Retrieve relevant context from vector database
        
        Args:
            query: User's question
            limit: Number of results to retrieve
            
        Returns:
            Tuple of (context_text, sources)
        """
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
        """
        Generate answer using LLM with retrieved context
        
        Args:
            query: User's question
            context: Retrieved context from documents
            
        Returns:
            Generated answer
        """
        prompt = f"""You are an expert assistant on autism spectrum disorder (ASD). 
Answer the following question based ONLY on the provided context from research documents.
If the context doesn't contain enough information to answer the question, say so.

Context from research documents:
{context}

Question: {query}

Provide a clear, accurate, and helpful answer based on the context above."""

        try:
            response = self.llm.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def query(self, question: str, reading_level: str = "grade_2", 
              show_sources: bool = True, show_original: bool = False) -> Dict:
        """
        Complete adaptive RAG query: retrieve, generate, and simplify
        
        Args:
            question: User's question
            reading_level: Target reading level ("grade_2", "original", or "both")
            show_sources: Whether to include sources
            show_original: Whether to show original answer along with simplified
            
        Returns:
            Dict with answers, sources, and metadata
        """
        # Step 1: Retrieve context
        print(f"🔍 Searching knowledge base...")
        context, sources = self.retrieve_context(question)
        
        if not context:
            return {
                'question': question,
                'answer': "I couldn't find relevant information in the knowledge base.",
                'simplified_answer': None,
                'sources': [],
                'success': False
            }
        
        print(f"✓ Found {len(sources)} relevant documents\n")
        
        # Step 2: Generate answer
        print("🤖 Generating answer...")
        original_answer = self.generate_answer(question, context)
        print("✓ Answer generated\n")
        
        # Step 3: Simplify to Grade 2 if requested
        simplified_answer = None
        simplification_metrics = None
        
        if reading_level in ["grade_2", "both"]:
            print("✏️  Simplifying to Grade 2 reading level...")
            simplification_result = self.adapter.simplify_text(
                original_answer, 
                context="autism information"
            )
            
            if simplification_result['success']:
                simplified_answer = simplification_result['simplified_text']
                simplification_metrics = simplification_result.get('metrics', {})
                print("✓ Simplification complete\n")
            else:
                print(f"⚠ Simplification failed: {simplification_result.get('error', 'Unknown error')}\n")
        
        # Prepare result
        result = {
            'question': question,
            'original_answer': original_answer if show_original or reading_level == "original" else None,
            'simplified_answer': simplified_answer,
            'answer': simplified_answer if reading_level == "grade_2" else original_answer,
            'sources': sources if show_sources else None,
            'success': True,
            'reading_level': reading_level,
            'metrics': simplification_metrics
        }
        
        return result
    
    def display_result(self, result: Dict):
        """
        Display query result in a formatted way
        
        Args:
            result: Result dictionary from query()
        """
        print(f"{'='*70}")
        print(f"Question: {result['question']}")
        print(f"{'='*70}\n")
        
        # Show simplified answer (primary)
        if result.get('simplified_answer'):
            print("📖 ANSWER (Grade 2 Reading Level):")
            print(f"{'='*70}")
            print(result['simplified_answer'])
            print(f"{'='*70}\n")
            
            # Show metrics
            if result.get('metrics'):
                print("📊 Readability Metrics:")
                for key, value in result['metrics'].items():
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
                print()
        
        # Show original if requested
        if result.get('original_answer'):
            print("📄 ORIGINAL ANSWER:")
            print(f"{'='*70}")
            print(result['original_answer'])
            print(f"{'='*70}\n")
        
        # Show sources
        if result.get('sources'):
            print(f"{'='*70}")
            print("📚 SOURCES:")
            print(f"{'='*70}\n")
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. {source['source']} (relevance: {source['score']:.4f})")
            print()
    
    def interactive_mode(self):
        """Interactive Q&A mode with content adaptation"""
        print(f"{'='*70}")
        print("ADAPTIVE RAG - INTERACTIVE MODE")
        print(f"{'='*70}\n")
        print("Ask questions about autism. Answers will be simplified to Grade 2 level.")
        print("\nCommands:")
        print("  'quit' or 'exit' - Exit")
        print("  'original' - Show both original and simplified answers")
        print("  'simple' - Show only simplified answers (default)")
        print(f"{'='*70}\n")
        
        mode = "simple"  # Default mode
        
        while True:
            try:
                user_input = input("Your question: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye!\n")
                    break
                
                if user_input.lower() == 'original':
                    mode = "both"
                    print("✓ Showing both original and simplified answers\n")
                    continue
                
                if user_input.lower() == 'simple':
                    mode = "simple"
                    print("✓ Showing only simplified answers\n")
                    continue
                
                # Process query
                result = self.query(
                    user_input,
                    reading_level="both" if mode == "both" else "grade_2",
                    show_original=mode == "both"
                )
                
                # Display result
                self.display_result(result)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                break
            except Exception as e:
                print(f"\n✗ Error: {str(e)}\n")


def main():
    """Main function for testing"""
    print("\n" + "="*70)
    print("ADAPTIVE RAG SYSTEM - AUTISM KNOWLEDGE BASE")
    print("="*70 + "\n")
    
    # Initialize system
    rag = AdaptiveRAG()
    
    # Choose mode
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
            "How is autism diagnosed?",
            "What are effective interventions for autism?",
        ]
        
        for question in sample_questions:
            result = rag.query(question, reading_level="both", show_original=True)
            rag.display_result(result)
            input("\nPress Enter for next question...")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
