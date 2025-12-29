"""
Orchestrator Agent
Coordinates all 4 agents to work together with parallel execution
- Runs agents in parallel for speed
- Aggregates results
- Generates PDF output
- Target: <30s total execution time
"""

import os
import time
from typing import Dict, List, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from dotenv import load_dotenv

# Import all agents
from agents.rag_retriever import RAGRetriever
from agents.content_adapter import ContentAdapter
from agents.social_story_agent import SocialStoryAgent
from agents.visual_generator import VisualGenerator

load_dotenv()

class Orchestrator:
    """
    Orchestrates all 4 AI agents to work together
    Supports parallel execution for speed
    """
    
    def __init__(self):
        """Initialize Orchestrator with all agents"""
        print("Initializing Orchestrator...")
        print("Loading all 4 agents...\n")
        
        start_time = time.time()
        
        # Initialize all agents
        self.rag_retriever = RAGRetriever()
        self.content_adapter = ContentAdapter()
        self.social_story_agent = SocialStoryAgent()
        self.visual_generator = VisualGenerator()
        
        init_time = time.time() - start_time
        
        print(f"\n✓ All agents initialized in {init_time:.2f}s")
        print("✓ Orchestrator ready!\n")
    
    def process_question(self, 
                        question: str,
                        generate_image: bool = True,
                        generate_social_story: bool = False,
                        child_name: str = "the child") -> Dict:
        """
        Process a question using all relevant agents in parallel
        
        Args:
            question: User's question about autism
            generate_image: Whether to generate an illustrative image
            generate_social_story: Whether to create a related social story
            child_name: Name for social story personalization
            
        Returns:
            Dict with all results aggregated
        """
        print(f"{'='*70}")
        print(f"PROCESSING: {question}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        results = {
            'question': question,
            'timestamp': datetime.now().isoformat(),
            'tasks_completed': []
        }
        
        # Task 1: RAG Retrieval (Required - must complete first)
        print("Step 1: Retrieving relevant information...")
        retrieval_start = time.time()
        
        rag_result = self.rag_retriever.retrieve(question, top_k=5)
        
        if rag_result['success']:
            context = "\n\n".join([r['text'] for r in rag_result['results']])
            sources = [{'source': r['source'], 'score': r['score']} for r in rag_result['results']]
            
            results['retrieval'] = {
                'success': True,
                'context': context,
                'sources': sources,
                'count': len(sources),
                'time': round(time.time() - retrieval_start, 2)
            }
            print(f"✓ Retrieved {len(sources)} documents ({results['retrieval']['time']}s)\n")
            results['tasks_completed'].append('retrieval')
        else:
            results['retrieval'] = {'success': False, 'error': rag_result['error']}
            print(f"✗ Retrieval failed\n")
            return results
        
        # Parallel Tasks: Run simultaneously for speed
        print("Step 2: Running parallel tasks...")
        parallel_start = time.time()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            
            # Task 2: Content Simplification (always run)
            futures['simplification'] = executor.submit(
                self._simplify_content,
                context[:1000]  # Limit context size for speed
            )
            
            # Task 3: Image Generation (optional)
            if generate_image:
                # Extract key terms for image prompt
                image_prompt = self._create_image_prompt(question)
                futures['image'] = executor.submit(
                    self._generate_image,
                    image_prompt
                )
            
            # Task 4: Social Story (optional)
            if generate_social_story:
                situation = self._extract_situation(question)
                futures['social_story'] = executor.submit(
                    self._create_social_story,
                    situation,
                    child_name
                )
            
            # Collect results as they complete
            for task_name, future in futures.items():
                try:
                    task_result = future.result(timeout=60)
                    results[task_name] = task_result
                    results['tasks_completed'].append(task_name)
                    print(f"✓ {task_name.title()}: {task_result.get('time', 0):.2f}s")
                except Exception as e:
                    results[task_name] = {'success': False, 'error': str(e)}
                    print(f"✗ {task_name.title()}: {str(e)}")
        
        parallel_time = time.time() - parallel_start
        print(f"\n✓ Parallel tasks completed in {parallel_time:.2f}s")
        
        # Total time
        total_time = time.time() - start_time
        results['total_time'] = round(total_time, 2)
        results['success'] = len(results['tasks_completed']) >= 2  # At least retrieval + simplification
        
        print(f"\n{'='*70}")
        print(f"TOTAL TIME: {total_time:.2f}s")
        print(f"{'='*70}\n")
        
        return results
    
    def _simplify_content(self, text: str) -> Dict:
        """Helper: Simplify content"""
        start = time.time()
        result = self.content_adapter.simplify_text(text, context="autism information")
        result['time'] = round(time.time() - start, 2)
        return result
    
    def _generate_image(self, prompt: str) -> Dict:
        """Helper: Generate image"""
        start = time.time()
        result = self.visual_generator.generate_image(prompt)
        result['time'] = round(time.time() - start, 2)
        return result
    
    def _create_social_story(self, situation: str, child_name: str) -> Dict:
        """Helper: Create social story"""
        start = time.time()
        result = self.social_story_agent.generate_social_story(situation, child_name)
        result['time'] = round(time.time() - start, 2)
        return result
    
    def _create_image_prompt(self, question: str) -> str:
        """Extract key concepts from question to create image prompt"""
        # Simple keyword extraction
        keywords = question.lower()
        
        if 'sensory' in keywords:
            return "child with autism using sensory toys, educational setting"
        elif 'communication' in keywords or 'talk' in keywords:
            return "child using communication cards, friendly setting"
        elif 'diagnosis' in keywords or 'doctor' in keywords:
            return "doctor meeting with child and parent, medical office"
        elif 'school' in keywords or 'classroom' in keywords:
            return "child in inclusive classroom, learning environment"
        else:
            return "diverse children with autism in educational setting"
    
    def _extract_situation(self, question: str) -> str:
        """Extract situation from question for social story"""
        # Simple situation extraction
        question_lower = question.lower()
        
        if 'doctor' in question_lower:
            return "going to the doctor"
        elif 'school' in question_lower:
            return "going to school"
        elif 'new' in question_lower and 'people' in question_lower:
            return "meeting new people"
        elif 'loud' in question_lower or 'noise' in question_lower:
            return "dealing with loud noises"
        else:
            return "learning new things"
    
    def generate_pdf_report(self, results: Dict, output_path: Optional[str] = None) -> Dict:
        """
        Generate PDF report from orchestrator results
        
        Args:
            results: Results from process_question()
            output_path: Custom output path (optional)
            
        Returns:
            Dict with PDF generation result
        """
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        # Generate output filename
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"autism_report_{timestamp}.pdf"
        
        print(f"\nGenerating PDF report...")
        
        try:
            # Create PDF
            doc = SimpleDocTemplate(str(output_path), pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#2C5F7F',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor='#2C5F7F',
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            story.append(Paragraph("Autism Education Report", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Question
            story.append(Paragraph(f"<b>Question:</b> {results['question']}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Simplified Answer
            if 'simplification' in results and results['simplification']['success']:
                story.append(Paragraph("Simple Explanation (Grade 2):", heading_style))
                simplified_text = results['simplification']['simplified_text']
                story.append(Paragraph(simplified_text, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Sources
            if 'retrieval' in results and results['retrieval']['success']:
                story.append(Paragraph("Sources:", heading_style))
                for i, source in enumerate(results['retrieval']['sources'][:5], 1):
                    source_text = f"{i}. {source['source']} (Relevance: {source['score']:.2f})"
                    story.append(Paragraph(source_text, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Image
            if 'image' in results and results['image']['success']:
                story.append(Paragraph("Educational Image:", heading_style))
                img_path = results['image']['image_path']
                if Path(img_path).exists():
                    img = RLImage(img_path, width=4*inch, height=4*inch)
                    story.append(img)
                story.append(Spacer(1, 0.2*inch))
            
            # Social Story
            if 'social_story' in results and results['social_story']['success']:
                story.append(Paragraph(f"Social Story: {results['social_story']['title']}", heading_style))
                story_text = results['social_story']['story']
                story.append(Paragraph(story_text.replace('\n', '<br/>'), styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Metadata
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))
            story.append(Paragraph(f"Total processing time: {results.get('total_time', 0)}s", styles['Italic']))
            
            # Build PDF
            doc.build(story)
            
            pdf_size = Path(output_path).stat().st_size / 1024  # KB
            
            return {
                'success': True,
                'pdf_path': str(output_path),
                'filename': Path(output_path).name,
                'size_kb': round(pdf_size, 2)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("ORCHESTRATOR TEST")
    print("="*70 + "\n")
    
    orchestrator = Orchestrator()
    
    # Process a question with all features
    print("Testing full orchestration...\n")
    
    results = orchestrator.process_question(
        question="How can I help my child with sensory processing issues?",
        generate_image=True,
        generate_social_story=True,
        child_name="Maya"
    )
    
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70 + "\n")
    
    print(f"Tasks completed: {', '.join(results['tasks_completed'])}")
    print(f"Total time: {results['total_time']}s")
    print(f"Success: {results['success']}")
    
    # Generate PDF
    print("\n" + "="*70)
    print("Generating PDF Report...")
    print("="*70 + "\n")
    
    pdf_result = orchestrator.generate_pdf_report(results)
    
    if pdf_result['success']:
        print(f"✓ PDF generated: {pdf_result['filename']}")
        print(f"✓ Size: {pdf_result['size_kb']} KB")
        print(f"✓ Path: {pdf_result['pdf_path']}")
    else:
        print(f"✗ PDF generation failed: {pdf_result['error']}")
# Project Complete: Dec 29, 2025
