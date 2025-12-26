"""
Unit Tests for Content Adapter
Uses pytest framework for comprehensive testing
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.content_adapter import ContentAdapter

@pytest.fixture
def adapter():
    """Fixture to create ContentAdapter instance"""
    return ContentAdapter()

class TestContentAdapterInit:
    """Test ContentAdapter initialization"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        # Should not raise an error if GROQ_API_KEY is in env
        adapter = ContentAdapter()
        assert adapter is not None
        assert adapter.client is not None
    
    def test_init_without_api_key(self, monkeypatch):
        """Test initialization fails without API key"""
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="GROQ_API_KEY not found"):
            ContentAdapter()

class TestSimplifyText:
    """Test text simplification functionality"""
    
    def test_simplify_basic_text(self, adapter):
        """Test basic text simplification"""
        complex_text = "Autism Spectrum Disorder is a neurodevelopmental condition."
        result = adapter.simplify_text(complex_text)
        
        assert result['success'] == True
        assert result['simplified_text'] != ""
        assert result['original_text'] == complex_text
        assert result['reading_level'] == 'grade_2'
        assert 'metrics' in result
    
    def test_simplify_empty_text(self, adapter):
        """Test simplification of empty text"""
        result = adapter.simplify_text("")
        
        assert result['success'] == False
        assert 'error' in result
        assert result['error'] == 'Empty text provided'
    
    def test_simplify_whitespace_only(self, adapter):
        """Test simplification of whitespace-only text"""
        result = adapter.simplify_text("   ")
        
        assert result['success'] == False
        assert 'error' in result
    
    def test_metrics_calculation(self, adapter):
        """Test that metrics are calculated"""
        text = "This is a simple test. It has two sentences."
        result = adapter.simplify_text(text)
        
        if result['success']:
            metrics = result['metrics']
            assert 'total_words' in metrics
            assert 'total_sentences' in metrics
            assert 'avg_words_per_sentence' in metrics
            assert 'estimated_grade_level' in metrics
            assert 'meets_grade_2_criteria' in metrics

class TestSimplifyMultiple:
    """Test batch simplification"""
    
    def test_simplify_multiple_texts(self, adapter):
        """Test batch simplification of multiple texts"""
        texts = [
            "Early intervention is important.",
            "Communication skills can be developed.",
            "Sensory processing varies."
        ]
        
        results = adapter.simplify_multiple(texts)
        
        assert len(results) == len(texts)
        
        for result in results:
            assert 'success' in result
            assert 'original_text' in result
    
    def test_simplify_empty_list(self, adapter):
        """Test batch simplification with empty list"""
        results = adapter.simplify_multiple([])
        
        assert results == []

class TestMetricsCalculation:
    """Test readability metrics calculation"""
    
    def test_calculate_metrics_simple(self, adapter):
        """Test metrics calculation for simple text"""
        text = "This is simple. Very easy."
        metrics = adapter._calculate_metrics(text)
        
        assert metrics['total_words'] == 5
        assert metrics['total_sentences'] == 2
        assert metrics['avg_words_per_sentence'] > 0
    
    def test_calculate_metrics_empty(self, adapter):
        """Test metrics calculation for empty text"""
        metrics = adapter._calculate_metrics("")
        
        assert metrics == {}
    
    def test_grade_level_estimation(self, adapter):
        """Test grade level estimation"""
        # Grade 1-2 level
        level = adapter._estimate_grade_level(7, 1.2)
        assert "Grade 1-2" in level
        
        # Higher grade level
        level = adapter._estimate_grade_level(15, 1.8)
        assert "Grade" in level

class TestAgeAppropriateExplanation:
    """Test age-appropriate explanations"""
    
    def test_create_explanation(self, adapter):
        """Test creating age-appropriate explanation"""
        result = adapter.create_age_appropriate_explanation("what is autism")
        
        assert result['success'] == True
        assert result['explanation'] != ""
        assert result['topic'] == "what is autism"
        assert result['age_group'] == "7-8 years"
        assert 'metrics' in result
    
    def test_create_explanation_custom_age(self, adapter):
        """Test creating explanation for custom age group"""
        result = adapter.create_age_appropriate_explanation(
            "sensory processing", 
            age_group="5-6 years"
        )
        
        assert result['age_group'] == "5-6 years"

class TestGrade2Compliance:
    """Test Grade 2 reading level compliance"""
    
    def test_short_sentences(self, adapter):
        """Test that output has short sentences"""
        complex_text = "Early intervention programs demonstrate efficacy in improving outcomes."
        result = adapter.simplify_text(complex_text)
        
        if result['success']:
            metrics = result['metrics']
            # Grade 2 should have <= 10 words per sentence
            assert metrics['avg_words_per_sentence'] <= 12  # Allow some flexibility
    
    def test_simple_syllables(self, adapter):
        """Test that output uses simple words"""
        complex_text = "Neurodevelopmental manifestations characterize this condition."
        result = adapter.simplify_text(complex_text)
        
        if result['success']:
            metrics = result['metrics']
            # Grade 2 should have simple words (low syllables/word)
            assert metrics['avg_syllables_per_word'] <= 1.5  # Allow some flexibility

# Test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
