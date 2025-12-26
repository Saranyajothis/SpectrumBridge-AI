"""
RAG Retriever Agent
Retrieves relevant autism information from vector database
Can be used independently or integrated with other agents
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

load_dotenv()

class RAGRetriever:
    """
    Retrieves relevant content from autism knowledge base using vector search
    """
    
    def __init__(self,
                 mongodb_uri: Optional[str] = None,
                 database_name: str = "spectrum_bridge_AI",
                 collection_name: str = "knowledge",
                 index_name: str = "vector_index",
                 model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG Retriever
        
        Args:
            mongodb_uri: MongoDB connection string
            database_name: Database name
            collection_name: Collection name
            index_name: Vector search index name
            model_name: Embedding model name
        """
        self.mongodb_uri = mongodb_uri or os.getenv("MONGODB_URI")
        
        if not self.mongodb_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        # MongoDB connection
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.index_name = index_name
        
        # Embedding model
        print(f"Loading embedding model: {model_name}...")
        self.embedding_model = SentenceTransformer(model_name)
        print("✓ RAG Retriever ready!")
    
    def retrieve(self, 
                query: str,
                top_k: int = 5,
                min_score: float = 0.0) -> Dict:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of results to return
            min_score: Minimum relevance score (0-1)
            
        Returns:
            Dict with 'results', 'query', 'count'
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Vector search pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.index_name,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 50,
                    "limit": top_k
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
        
        try:
            results = list(self.collection.aggregate(pipeline))
            
            # Filter by minimum score
            filtered_results = [
                r for r in results 
                if r.get('score', 0) >= min_score
            ]
            
            # Format results
            formatted_results = []
            for result in filtered_results:
                formatted_results.append({
                    'text': result['text'],
                    'source': result['metadata']['source'],
                    'score': result.get('score', 0),
                    'chunk_id': result['metadata'].get('chunk_id', 0)
                })
            
            return {
                'success': True,
                'query': query,
                'results': formatted_results,
                'count': len(formatted_results)
            }
            
        except Exception as e:
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'count': 0,
                'results': []
            }
    
    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve and combine context as a single string
        Useful for feeding to LLMs
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            Combined context string
        """
        retrieval = self.retrieve(query, top_k)
        
        if not retrieval['success'] or not retrieval['results']:
            return ""
        
        # Combine all retrieved texts
        context_parts = [r['text'] for r in retrieval['results']]
        return "\n\n".join(context_parts)
    
    def retrieve_by_topic(self, topic: str, top_k: int = 10) -> Dict:
        """
        Retrieve documents related to a specific topic
        
        Args:
            topic: Topic keyword (e.g., "diagnosis", "intervention", "sensory")
            top_k: Number of results
            
        Returns:
            Dict with results grouped by source
        """
        retrieval = self.retrieve(topic, top_k)
        
        if not retrieval['success']:
            return retrieval
        
        # Group by source
        by_source = {}
        for result in retrieval['results']:
            source = result['source']
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(result)
        
        return {
            'success': True,
            'topic': topic,
            'results_by_source': by_source,
            'total_sources': len(by_source),
            'total_chunks': len(retrieval['results'])
        }
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the knowledge base
        
        Returns:
            Dict with database statistics
        """
        try:
            total_docs = self.collection.count_documents({})
            
            # Get unique sources
            pipeline = [
                {"$group": {"_id": "$metadata.source", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            
            sources = list(self.collection.aggregate(pipeline))
            
            return {
                'success': True,
                'total_documents': total_docs,
                'unique_sources': len(sources),
                'sources': [
                    {'name': s['_id'], 'chunks': s['count']}
                    for s in sources
                ]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_by_source(self, source_name: str, limit: int = 10) -> Dict:
        """
        Get all chunks from a specific source document
        
        Args:
            source_name: PDF filename
            limit: Maximum chunks to return
            
        Returns:
            Dict with results from that source
        """
        try:
            results = list(self.collection.find(
                {"metadata.source": source_name},
                {"text": 1, "metadata": 1}
            ).limit(limit))
            
            formatted = [
                {
                    'text': r['text'],
                    'chunk_id': r['metadata'].get('chunk_id', 0)
                }
                for r in results
            ]
            
            return {
                'success': True,
                'source': source_name,
                'results': formatted,
                'count': len(formatted)
            }
            
        except Exception as e:
            return {
                'success': False,
                'source': source_name,
                'error': str(e)
            }


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("RAG RETRIEVER AGENT TEST")
    print("="*70 + "\n")
    
    retriever = RAGRetriever()
    
    # Test 1: Retrieve relevant documents
    print("Test 1: Retrieve documents for 'early signs of autism'\n")
    
    result = retriever.retrieve("early signs of autism", top_k=3)
    
    if result['success']:
        print(f"✓ Found {result['count']} relevant documents\n")
        for i, doc in enumerate(result['results'], 1):
            print(f"{i}. [{doc['source']}] (Score: {doc['score']:.4f})")
            print(f"   {doc['text'][:150]}...\n")
    else:
        print(f"❌ Failed: {result['error']}")
    
    # Test 2: Get statistics
    print("\n" + "="*70)
    print("Test 2: Knowledge Base Statistics\n")
    
    stats = retriever.get_statistics()
    
    if stats['success']:
        print(f"✓ Total documents: {stats['total_documents']}")
        print(f"✓ Unique sources: {stats['unique_sources']}")
        print(f"\nTop 5 sources:")
        for source in stats['sources'][:5]:
            print(f"  • {source['name']}: {source['chunks']} chunks")
    else:
        print(f"❌ Failed: {stats['error']}")
