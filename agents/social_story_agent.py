"""
Social Story Agent
Generates autism-friendly social stories using Groq API
Social stories help autistic children understand social situations
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class SocialStoryAgent:
    """
    Creates structured social stories for autism education
    Social stories follow Carol Gray's framework
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Social Story Agent with Groq API
        
        Args:
            api_key: Groq API key (optional, reads from env)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        
        # Social story guidelines (Carol Gray framework)
        self.social_story_guidelines = """
SOCIAL STORY FRAMEWORK (Carol Gray):
1. Descriptive sentences: What happens, where, when, who
2. Perspective sentences: How others feel or think
3. Directive sentences: What the child should do
4. Affirmative sentences: Reassurance and positive outcomes

RULES:
- Use first person ("I") or third person for the child
- Present or future tense
- Positive, reassuring tone
- 5-10 sentences total
- Clear, simple language
- Include what to expect and how to respond
"""
    
    def generate_social_story(self, 
                             situation: str,
                             child_name: str = "the child",
                             reading_level: str = "grade_2") -> Dict:
        """
        Generate a social story for a specific situation
        
        Args:
            situation: The social situation to explain (e.g., "going to the doctor")
            child_name: Name to use in the story (default: "the child")
            reading_level: Target reading level (grade_2, grade_3, etc.)
            
        Returns:
            Dict with 'story', 'title', 'situation', 'success'
        """
        
        # Adjust language based on reading level
        language_guide = {
            'grade_2': 'Use very simple words (5-8 words per sentence)',
            'grade_3': 'Use simple words (8-12 words per sentence)',
            'grade_4': 'Use clear language (10-15 words per sentence)'
        }
        
        lang_instruction = language_guide.get(reading_level, language_guide['grade_2'])
        
        prompt = f"""Create a social story about: {situation}

Child's name: {child_name}
Reading level: {reading_level}

{self.social_story_guidelines}

Language: {lang_instruction}

Write a complete social story with:
1. A clear title
2. 5-10 sentences following the framework above
3. Positive, reassuring tone
4. Practical guidance

Format:
Title: [Clear, simple title]

[The story - 5-10 sentences]

Respond with ONLY the title and story, no preamble."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in creating social stories for autistic children following Carol Gray's framework. Write clear, positive, helpful stories."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=512
            )
            
            response = chat_completion.choices[0].message.content.strip()
            
            # Parse title and story
            lines = response.split('\n')
            title = ""
            story_lines = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                elif line and not line.startswith("Title"):
                    story_lines.append(line)
            
            story = '\n'.join(story_lines).strip()
            
            if not title:
                title = f"About {situation.title()}"
            
            return {
                'success': True,
                'title': title,
                'story': story,
                'situation': situation,
                'child_name': child_name,
                'reading_level': reading_level,
                'full_text': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'situation': situation,
                'child_name': child_name,
                'reading_level': reading_level
            }
    
    def generate_common_situations(self, child_name: str = "I") -> List[Dict]:
        """
        Generate social stories for common autism-related situations
        
        Args:
            child_name: Name to use (default: "I" for first person)
            
        Returns:
            List of social stories
        """
        common_situations = [
            "going to the doctor",
            "trying new foods",
            "meeting new people",
            "dealing with loud noises",
            "waiting my turn",
            "asking for help",
            "feeling overwhelmed",
            "making friends"
        ]
        
        stories = []
        
        for situation in common_situations:
            print(f"Generating story: {situation}...")
            story = self.generate_social_story(situation, child_name)
            if story['success']:
                stories.append(story)
                print(f"✓ Generated: {story['title']}")
            else:
                print(f"✗ Failed: {situation}")
        
        return stories
    
    def customize_story(self, 
                       base_story: str,
                       child_name: str,
                       specific_details: str) -> Dict:
        """
        Customize an existing social story with specific details
        
        Args:
            base_story: The base social story text
            child_name: Child's name
            specific_details: Specific details to add (e.g., "at Dr. Smith's office")
            
        Returns:
            Dict with customized story
        """
        
        prompt = f"""Customize this social story for a specific child:

Base Story:
{base_story}

Customization:
- Child's name: {child_name}
- Specific details: {specific_details}

Rewrite the story with these personalizations while keeping the same structure and tone.

Respond with ONLY the customized story:"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You customize social stories for autistic children. Keep the positive tone and structure."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=512
            )
            
            customized_story = chat_completion.choices[0].message.content.strip()
            
            return {
                'success': True,
                'story': customized_story,
                'child_name': child_name,
                'specific_details': specific_details
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("SOCIAL STORY AGENT TEST")
    print("="*70 + "\n")
    
    agent = SocialStoryAgent()
    
    # Test 1: Generate a social story
    print("Test 1: Generate social story for 'going to the doctor'\n")
    
    result = agent.generate_social_story("going to the doctor", child_name="Alex")
    
    if result['success']:
        print(f"Title: {result['title']}\n")
        print(f"Story:\n{result['story']}\n")
        print("✅ Social story generated successfully!")
    else:
        print(f"❌ Failed: {result['error']}")
