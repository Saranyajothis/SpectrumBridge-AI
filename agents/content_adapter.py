"""
Content Adapter Agent
Simplifies complex autism-related content to Grade 2 reading level using Groq
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

class ContentAdapter:
    """
    Adapts complex content to Grade 2 reading level for better accessibility
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Content Adapter with Groq API
        
        Args:
            api_key: Groq API key (optional, reads from env if not provided)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Configure Groq
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def simplify_text(self, text: str, context: str = "autism information") -> Dict:
        """
        Simplify complex text to Grade 2 reading level
        
        Args:
            text: Complex text to simplify
            context: Context about the content (helps with accurate simplification)
            
        Returns:
            Dict with 'simplified_text', 'original_text', 'reading_level'
        """
        
        if not text or not text.strip():
            return {
                'simplified_text': '',
                'original_text': text,
                'reading_level': 'grade_2',
                'success': False,
                'error': 'Empty text provided'
            }
        
        # Ultra-strict Grade 2 prompt
        prompt = f"""Rewrite this text for a 7-year-old child. 

RULES (MUST FOLLOW):
1. Use ONLY 1-syllable words (like: kid, talk, play, run, see, help, good)
2. MAXIMUM 6 words per sentence
3. Start new sentence for each idea
4. Use simple grammar: subject + verb + object
5. No commas, just periods
6. Sound like a child talking

TEXT TO SIMPLIFY:
{text}

EXAMPLES OF GOOD GRADE 2:
"Some kids are different."
"They talk their own way."
"This is called autism."
"They are good kids."

YOUR TURN - Write it simply (respond with ONLY the simple text):"""

        try:
            # Generate simplified content
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You simplify text to Grade 2 level. Use tiny words. Make tiny sentences. Sound like a 7 year old."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.1,  # Almost deterministic for consistency
                max_tokens=300  # Force brevity
            )
            
            simplified = chat_completion.choices[0].message.content.strip()
            
            # Calculate metrics
            metrics = self._calculate_metrics(simplified)
            
            return {
                'simplified_text': simplified,
                'original_text': text,
                'reading_level': 'grade_2',
                'success': True,
                'metrics': metrics
            }
            
        except Exception as e:
            return {
                'simplified_text': '',
                'original_text': text,
                'reading_level': 'grade_2',
                'success': False,
                'error': str(e)
            }
    
    def simplify_multiple(self, texts: List[str], context: str = "autism information") -> List[Dict]:
        """
        Simplify multiple texts in batch
        
        Args:
            texts: List of complex texts to simplify
            context: Context about the content
            
        Returns:
            List of simplification results
        """
        results = []
        
        for text in texts:
            result = self.simplify_text(text, context)
            results.append(result)
        
        return results
    
    def _calculate_metrics(self, text: str) -> Dict:
        """
        Calculate readability metrics for simplified text
        
        Args:
            text: Simplified text
            
        Returns:
            Dict with various readability metrics
        """
        if not text:
            return {}
        
        # Count sentences (approximate)
        sentences = text.count('.') + text.count('!') + text.count('?')
        sentences = max(1, sentences)
        
        # Count words
        words = len(text.split())
        
        # Count syllables (improved algorithm)
        words_list = text.lower().split()
        syllables = 0
        for word in words_list:
            # Remove punctuation
            word = ''.join(c for c in word if c.isalpha())
            if not word:
                continue
                
            # Simple syllable counter
            count = 0
            prev_was_vowel = False
            for char in word:
                is_vowel = char in 'aeiouy'  # Include 'y' as vowel
                if is_vowel and not prev_was_vowel:
                    count += 1
                prev_was_vowel = is_vowel
            
            # Silent 'e' at end doesn't count
            if word.endswith('e') and count > 1:
                count -= 1
            
            # Every word has at least 1 syllable
            syllables += max(1, count)
        
        # Average words per sentence
        avg_words_per_sentence = words / sentences if sentences > 0 else 0
        
        # Average syllables per word
        avg_syllables_per_word = syllables / words if words > 0 else 0
        
        # Check if meets STRICT Grade 2 criteria
        meets_criteria = avg_words_per_sentence <= 8 and avg_syllables_per_word <= 1.2
        
        return {
            'total_words': words,
            'total_sentences': sentences,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 1),
            'estimated_grade_level': self._estimate_grade_level(avg_words_per_sentence, avg_syllables_per_word),
            'meets_grade_2_criteria': meets_criteria
        }
    
    def _estimate_grade_level(self, avg_words: float, avg_syllables: float) -> str:
        """
        Estimate reading grade level based on metrics
        
        Args:
            avg_words: Average words per sentence
            avg_syllables: Average syllables per word
            
        Returns:
            Estimated grade level string
        """
        # Strict grade level estimation
        if avg_words <= 8 and avg_syllables <= 1.2:
            return "Grade 1-2 ✓"
        elif avg_words <= 10 and avg_syllables <= 1.4:
            return "Grade 3-4"
        elif avg_words <= 15:
            return "Grade 5-6"
        else:
            return "Grade 7+"
    
    def create_age_appropriate_explanation(self, topic: str, age_group: str = "7-8 years") -> Dict:
        """
        Create age-appropriate explanation of autism-related topics
        
        Args:
            topic: Topic to explain
            age_group: Target age group
            
        Returns:
            Dict with explanation and metadata
        """
        
        prompt = f"""Explain "{topic}" to a 7-year-old child.

RULES:
- Use only 1-syllable words
- Maximum 6 words per sentence
- Be positive and simple
- Sound like a child talking

Write the explanation (short and simple):"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Explain things simply to 7 year olds. Use tiny words. Use tiny sentences."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=200
            )
            
            explanation = chat_completion.choices[0].message.content.strip()
            
            metrics = self._calculate_metrics(explanation)
            
            return {
                'explanation': explanation,
                'topic': topic,
                'age_group': age_group,
                'reading_level': 'grade_2',
                'success': True,
                'metrics': metrics
            }
            
        except Exception as e:
            return {
                'explanation': '',
                'topic': topic,
                'age_group': age_group,
                'reading_level': 'grade_2',
                'success': False,
                'error': str(e)
            }


# Example usage
if __name__ == "__main__":
    adapter = ContentAdapter()
    
    complex_text = """
    Autism Spectrum Disorder is a neurodevelopmental condition characterized by 
    persistent deficits in social communication and social interaction across 
    multiple contexts, as well as restricted, repetitive patterns of behavior, 
    interests, or activities.
    """
    
    print("="*70)
    print("CONTENT ADAPTER TEST (Strict Grade 2)")
    print("="*70 + "\n")
    
    result = adapter.simplify_text(complex_text)
    
    if result['success']:
        print("Original:")
        print(complex_text.strip())
        print("\nSimplified (Grade 2):")
        print(result['simplified_text'])
        print("\nMetrics:")
        for key, value in result['metrics'].items():
            print(f"  {key}: {value}")
    else:
        print(f"Error: {result['error']}")
