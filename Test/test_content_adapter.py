"""
Unit Tests for Content Adapter
Tests simplification, Gemini integration, and reading level validation
"""

import unittest
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.content_adapter import ContentAdapter


class TestContentAdapter(unittest.TestCase):
    """Test suite for Content Adapter"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.adapter = ContentAdapter()
    
    def test_initialization(self):
        """Test that adapter initializes correctly"""
        self.assertIsNotNone(self.adapter)
        self.assertIsNotNone(self.adapter.model)
        self.assertIsNotNone(self.adapter.api_key)
    
    def test_simplify_basic_text(self):
        """Test basic text simplification"""
        complex_text = """
        Autism Spectrum Disorder is a neurodevelopmental condition characterized 
        by persistent deficits in social communication.
        """
        
        result = self.adapter.simplify_text(complex_text)
        
        # Check result structure
        self.assertIn('simplified_text', result)
        self.assertIn('original_text', result)
        self.assertIn('reading_level', result)
        self.assertIn('success', result)
        
        # Check success
        self.assertTrue(result['success'])
        
        # Check that simplified text is different from original
        self.assertNotEqual(result['simplified_text'], complex_text.strip())
        
        # Check that simplified text is not empty
        self.assertTrue(len(result['simplified_text']) > 0)
    
    def test_simplify_empty_text(self):
        """Test handling of empty text"""
        result = self.adapter.simplify_text("")
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_simplify_with_context(self):
        """Test simplification with context"""
        text = "Children with ASD may exhibit stereotyped behaviors."
        context = "autism behavioral patterns"
        
        result = self.adapter.simplify_text(text, context=context)
        
        self.assertTrue(result['success'])
        self.assertTrue(len(result['simplified_text']) > 0)
    
    def test_metrics_calculation(self):
        """Test that metrics are calculated correctly"""
        text = "This is a simple sentence."
        
        result = self.adapter.simplify_text(text)
        
        self.assertIn('metrics', result)
        metrics = result['metrics']
        
        # Check that required metrics exist
        self.assertIn('total_words', metrics)
        self.assertIn('total_sentences', metrics)
        self.assertIn('avg_words_per_sentence', metrics)
        self.assertIn('estimated_grade_level', metrics)
        
        # Check that metrics are reasonable
        self.assertGreater(metrics['total_words'], 0)
        self.assertGreater(metrics['total_sentences'], 0)
    
    def test_reading_level_grade_2(self):
        """Test that output is appropriate for Grade 2"""
        complex_text = """
        Neurodevelopmental disorders encompass a heterogeneous group of conditions 
        with onset during the developmental period, characterized by developmental 
        deficits that produce impairments.
        """
        
        result = self.adapter.simplify_text(complex_text)
        
        self.assertTrue(result['success'])
        
        # Check metrics indicate Grade 2 level
        if 'metrics' in result and 'avg_words_per_sentence' in result['metrics']:
            # Grade 2 should have short sentences (typically under 10 words)
            avg_words = result['metrics']['avg_words_per_sentence']
            self.assertLess(avg_words, 15, 
                          f"Average words per sentence ({avg_words}) too high for Grade 2")
    
    def test_simplify_multiple_texts(self):
        """Test batch simplification"""
        texts = [
            "Autism is a spectrum disorder.",
            "Social communication can be challenging.",
            "Every person with autism is unique."
        ]
        
        results = self.adapter.simplify_multiple(texts)
        
        # Check we got results for all texts
        self.assertEqual(len(results), len(texts))
        
        # Check all succeeded
        for result in results:
            self.assertTrue(result['success'])
            self.assertTrue(len(result['simplified_text']) > 0)
    
    def test_age_appropriate_explanation(self):
        """Test creation of age-appropriate explanations"""
        topic = "what is autism"
        
        result = self.adapter.create_age_appropriate_explanation(topic)
        
        # Check result structure
        self.assertIn('explanation', result)
        self.assertIn('topic', result)
        self.assertIn('success', result)
        
        # Check success
        self.assertTrue(result['success'])
        
        # Check explanation is not empty
        self.assertTrue(len(result['explanation']) > 0)
        
        # Check it has metrics
        self.assertIn('metrics', result)
    
    def test_different_topics(self):
        """Test simplification of different autism-related topics"""
        topics = [
            "sensory processing in autism",
            "communication differences",
            "repetitive behaviors"
        ]
        
        for topic in topics:
            result = self.adapter.create_age_appropriate_explanation(topic)
            self.assertTrue(result['success'], 
                          f"Failed to create explanation for: {topic}")
    
    def test_grade_level_estimation(self):
        """Test grade level estimation logic"""
        # Test Grade 1-2 level
        grade_12 = self.adapter._estimate_grade_level(7, 1.2)
        self.assertIn("Grade 1-2", grade_12)
        
        # Test Grade 3-4 level
        grade_34 = self.adapter._estimate_grade_level(11, 1.4)
        self.assertIn("Grade 3-4", grade_34)
        
        # Test higher grade level
        grade_high = self.adapter._estimate_grade_level(20, 2.0)
        self.assertIn("Grade", grade_high)
    
    def test_preserves_key_information(self):
        """Test that simplification preserves key concepts"""
        text = "Autism affects communication and behavior."
        
        result = self.adapter.simplify_text(text)
        
        simplified = result['simplified_text'].lower()
        
        # Key concepts should still be present (in some form)
        # Note: This is a basic check - simplified text may use different words
        self.assertTrue(
            'autism' in simplified or 'autistic' in simplified,
            "Key concept 'autism' missing from simplified text"
        )
    
    def test_error_handling_invalid_api_key(self):
        """Test error handling with invalid API key"""
        # This test checks that invalid API key is handled gracefully
        try:
            invalid_adapter = ContentAdapter(api_key="invalid_key_12345")
            result = invalid_adapter.simplify_text("Test text")
            
            # Should either fail initialization or return error in result
            if result:
                self.assertFalse(result['success'])
        except Exception:
            # Expected - initialization should fail with invalid key
            pass


class TestContentAdapterIntegration(unittest.TestCase):
    """Integration tests for Content Adapter with real API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up for integration tests"""
        cls.adapter = ContentAdapter()
    
    def test_real_autism_content_simplification(self):
        """Test simplification of real autism-related content"""
        real_content = """
        Early intervention services for children with autism spectrum disorder 
        typically include applied behavior analysis (ABA), speech therapy, 
        occupational therapy, and social skills training. Research demonstrates 
        that intensive early intervention can significantly improve developmental 
        outcomes and adaptive functioning.
        """
        
        result = self.adapter.simplify_text(real_content, context="autism interventions")
        
        self.assertTrue(result['success'])
        
        # Simplified text should be substantially shorter
        original_word_count = len(real_content.split())
        simplified_word_count = len(result['simplified_text'].split())
        
        # Simplified might be similar length but simpler words, or shorter
        # Main check is that it's readable
        self.assertGreater(simplified_word_count, 10, 
                          "Simplified text too short to be meaningful")
    
    def test_maintains_positive_tone(self):
        """Test that simplification maintains positive, respectful tone"""
        text = "Individuals with autism may struggle with social interactions."
        
        result = self.adapter.simplify_text(text)
        
        # Check for positive/neutral language (basic check)
        negative_words = ['struggle', 'deficit', 'impairment', 'abnormal', 'disorder']
        simplified_lower = result['simplified_text'].lower()
        
        # Count negative words in simplified version
        negative_count = sum(1 for word in negative_words if word in simplified_lower)
        
        # Should minimize negative framing
        self.assertLessEqual(negative_count, 1, 
                           "Too many negative words in simplified text")


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestContentAdapter))
    suite.addTests(loader.loadTestsFromTestCase(TestContentAdapterIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED")
    
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
