"""
Unit Tests for Social Story Agent and RAG Retriever
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.social_story_agent import SocialStoryAgent
from agents.rag_retriever import RAGRetriever

# Social Story Agent Tests

@pytest.fixture
def social_story_agent():
    """Fixture for Social Story Agent"""
    return SocialStoryAgent()

class TestSocialStoryAgent:
    """Test Social Story Agent"""
    
    def test_init(self, social_story_agent):
        """Test initialization"""
        assert social_story_agent is not None
        assert social_story_agent.client is not None
    
    def test_generate_social_story(self, social_story_agent):
        """Test social story generation"""
        result = social_story_agent.generate_social_story("waiting my turn")
        
        assert result['success'] == True
        assert 'title' in result
        assert 'story' in result
        assert result['situation'] == "waiting my turn"
    
    def test_social_story_with_custom_name(self, social_story_agent):
        """Test social story with custom child name"""
        result = social_story_agent.generate_social_story("going to school", child_name="Alex")
        
        assert result['success'] == True
        assert result['child_name'] == "Alex"
    
    def test_different_reading_levels(self, social_story_agent):
        """Test different reading levels"""
        result_grade2 = social_story_agent.generate_social_story("making friends", reading_level="grade_2")
        result_grade3 = social_story_agent.generate_social_story("making friends", reading_level="grade_3")
        
        assert result_grade2['success'] == True
        assert result_grade3['success'] == True
        assert result_grade2['reading_level'] == "grade_2"
        assert result_grade3['reading_level'] == "grade_3"

# RAG Retriever Tests

@pytest.fixture
def rag_retriever():
    """Fixture for RAG Retriever"""
    return RAGRetriever()

class TestRAGRetriever:
    """Test RAG Retriever Agent"""
    
    def test_init(self, rag_retriever):
        """Test initialization"""
        assert rag_retriever is not None
        assert rag_retriever.collection is not None
        assert rag_retriever.embedding_model is not None
    
    def test_retrieve(self, rag_retriever):
        """Test document retrieval"""
        result = rag_retriever.retrieve("autism diagnosis", top_k=3)
        
        assert result['success'] == True
        assert 'results' in result
        assert 'count' in result
        assert result['query'] == "autism diagnosis"
    
    def test_retrieve_context(self, rag_retriever):
        """Test context retrieval as string"""
        context = rag_retriever.retrieve_context("early signs autism", top_k=2)
        
        assert isinstance(context, str)
        # Context might be empty if database is empty, that's ok
    
    def test_retrieve_by_topic(self, rag_retriever):
        """Test topic-based retrieval"""
        result = rag_retriever.retrieve_by_topic("intervention", top_k=5)
        
        assert result['success'] == True
        assert 'results_by_source' in result
        assert 'total_sources' in result
    
    def test_get_statistics(self, rag_retriever):
        """Test database statistics"""
        stats = rag_retriever.get_statistics()
        
        assert stats['success'] == True
        assert 'total_documents' in stats
        assert 'unique_sources' in stats
    
    def test_search_by_source(self, rag_retriever):
        """Test searching within a specific source"""
        # First get a source name
        stats = rag_retriever.get_statistics()
        
        if stats['success'] and len(stats['sources']) > 0:
            source_name = stats['sources'][0]['name']
            result = rag_retriever.search_by_source(source_name, limit=5)
            
            assert result['success'] == True
            assert result['source'] == source_name

class TestAgentIntegration:
    """Test that agents can work together"""
    
    def test_rag_to_content_adapter(self, rag_retriever):
        """Test RAG → Content Adapter pipeline"""
        # Retrieve content
        context = rag_retriever.retrieve_context("autism", top_k=1)
        
        if context:
            # Simplify it
            adapter = ContentAdapter()
            result = adapter.simplify_text(context[:500])  # First 500 chars
            
            assert result['success'] == True
    
    def test_social_story_independent(self):
        """Test Social Story works without RAG"""
        agent = SocialStoryAgent()
        result = agent.generate_social_story("brushing teeth")
        
        assert result['success'] == True

# Test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
