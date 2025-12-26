# 📚 API Reference

## Agent APIs

All agents can be used programmatically via Python imports or through the MCP server.

---

## 1. RAG Retriever

### Import
```python
from agents.rag_retriever import RAGRetriever
```

### Initialize
```python
retriever = RAGRetriever(
    database_name="spectrum_bridge_AI",
    collection_name="knowledge_base",
    index_name="vector_index"
)
```

### Methods

#### `retrieve(query, top_k=5, min_score=0.0)`
Search the knowledge base.

**Parameters:**
- `query` (str): Search query
- `top_k` (int): Number of results (default: 5)
- `min_score` (float): Minimum relevance score (0-1)

**Returns:**
```python
{
    'success': True,
    'query': 'early signs autism',
    'results': [
        {
            'text': 'Document text...',
            'source': 'CDC_Diagnosis_Guide.pdf',
            'score': 0.8494,
            'chunk_id': 0
        },
        ...
    ],
    'count': 5
}
```

**Example:**
```python
result = retriever.retrieve("autism diagnosis", top_k=3)
for doc in result['results']:
    print(f"{doc['source']}: {doc['score']:.2f}")
```

#### `retrieve_context(query, top_k=5)`
Get combined context as string (for LLM input).

**Returns:** `str` - Combined text from all retrieved documents

**Example:**
```python
context = retriever.retrieve_context("sensory processing")
# Use context with LLM
```

#### `get_statistics()`
Get knowledge base statistics.

**Returns:**
```python
{
    'success': True,
    'total_documents': 4275,
    'unique_sources': 22,
    'sources': [
        {'name': 'NAC_Evidence_Based_Practices.pdf', 'chunks': 1154},
        ...
    ]
}
```

---

## 2. Content Adapter

### Import
```python
from agents.content_adapter import ContentAdapter
```

### Initialize
```python
adapter = ContentAdapter()
```

### Methods

#### `simplify_text(text, context='autism information')`
Simplify text to Grade 2 reading level.

**Parameters:**
- `text` (str): Complex text to simplify
- `context` (str): Context hint for better simplification

**Returns:**
```python
{
    'success': True,
    'simplified_text': 'Some kids are different. They talk their own way.',
    'original_text': 'Autism Spectrum Disorder is...',
    'reading_level': 'grade_2',
    'metrics': {
        'total_words': 24,
        'total_sentences': 6,
        'avg_words_per_sentence': 4.0,
        'avg_syllables_per_word': 1.2,
        'estimated_grade_level': 'Grade 1-2 ✓',
        'meets_grade_2_criteria': True
    }
}
```

**Example:**
```python
result = adapter.simplify_text(
    "Autism involves persistent challenges in social communication."
)
print(result['simplified_text'])
print(f"Grade level: {result['metrics']['estimated_grade_level']}")
```

#### `simplify_multiple(texts, context='autism information')`
Batch simplification.

**Parameters:**
- `texts` (List[str]): List of texts to simplify

**Returns:** `List[Dict]` - List of simplification results

---

## 3. Social Story Agent

### Import
```python
from agents.social_story_agent import SocialStoryAgent
```

### Initialize
```python
agent = SocialStoryAgent()
```

### Methods

#### `generate_social_story(situation, child_name='I', reading_level='grade_2')`
Generate a social story.

**Parameters:**
- `situation` (str): Situation to explain
- `child_name` (str): Child's name for personalization
- `reading_level` (str): 'grade_2', 'grade_3', or 'grade_4'

**Returns:**
```python
{
    'success': True,
    'title': 'Going to the Doctor',
    'story': 'I go to the doctor. The doctor is nice. They check me...',
    'situation': 'going to the doctor',
    'child_name': 'Emma',
    'reading_level': 'grade_2',
    'metrics': {...}
}
```

**Example:**
```python
story = agent.generate_social_story(
    situation="waiting my turn",
    child_name="Alex",
    reading_level="grade_2"
)
print(story['title'])
print(story['story'])
```

#### `generate_common_situations(child_name='I')`
Generate stories for 8 common situations.

**Returns:** `List[Dict]` - List of social stories

---

## 4. Visual Generator

### Import
```python
from agents.visual_generator import VisualGenerator
```

### Initialize
```python
generator = VisualGenerator()
```

### Methods

#### `generate_image(prompt, filename=None)`
Generate a single educational image.

**Parameters:**
- `prompt` (str): Image description
- `filename` (str, optional): Custom filename

**Returns:**
```python
{
    'success': True,
    'image_path': '/path/to/image.png',
    'filename': '20251228_123456_child_playing.png',
    'prompt': 'happy child playing with blocks',
    'generation_time': 45.2,
    'size': '512x512',
    'method': 'stable_diffusion_local'
}
```

**Example:**
```python
result = generator.generate_image(
    "child with autism using communication cards"
)
print(f"Image saved: {result['filename']}")
print(f"Time: {result['generation_time']}s")
```

#### `generate_batch(prompts)`
Generate multiple images.

**Parameters:**
- `prompts` (List[str]): List of image descriptions

**Returns:** `List[Dict]` - List of generation results

#### `generate_autism_educational_images(topic='general')`
Generate themed image set.

**Parameters:**
- `topic` (str): 'general', 'sensory', 'communication', or 'social'

**Returns:** `List[Dict]` - 5 themed images

---

## 5. Orchestrator

### Import
```python
from agents.orchestrator import Orchestrator
```

### Initialize
```python
orch = Orchestrator()
```

### Methods

#### `process_question(question, generate_image=True, generate_social_story=False, child_name='the child')`
Coordinate all agents for a complete response.

**Parameters:**
- `question` (str): User's question
- `generate_image` (bool): Generate illustrative image
- `generate_social_story` (bool): Create related social story
- `child_name` (str): Name for social story

**Returns:**
```python
{
    'question': 'How is autism diagnosed?',
    'timestamp': '2024-12-28T20:00:00',
    'tasks_completed': ['retrieval', 'simplification', 'social_story'],
    'retrieval': {...},
    'simplification': {...},
    'social_story': {...},
    'image': {...},
    'total_time': 8.5,
    'success': True
}
```

**Example:**
```python
results = orch.process_question(
    question="What are sensory processing issues in autism?",
    generate_image=False,
    generate_social_story=True,
    child_name="Maya"
)

print(f"Completed in {results['total_time']}s")
print(f"Tasks: {results['tasks_completed']}")
```

#### `generate_pdf_report(results, output_path=None)`
Generate PDF report from results.

**Parameters:**
- `results` (Dict): Results from process_question()
- `output_path` (str, optional): Custom PDF path

**Returns:**
```python
{
    'success': True,
    'pdf_path': '/path/to/report.pdf',
    'filename': 'autism_report_20251228.pdf',
    'size_kb': 125.5
}
```

---

## MCP Server API

### Tools Available

All tools accessible via Claude Desktop or MCP protocol.

#### 1. search_autism_knowledge
```json
{
  "query": "early signs of autism",
  "top_k": 5
}
```

#### 2. simplify_content
```json
{
  "text": "Complex autism text here..."
}
```

#### 3. generate_social_story
```json
{
  "situation": "going to school",
  "child_name": "Emma",
  "reading_level": "grade_2"
}
```

#### 4. generate_educational_image
```json
{
  "prompt": "child with autism playing"
}
```

#### 5. answer_question
```json
{
  "question": "What is autism?",
  "simplify": true
}
```

#### 6. create_full_report
```json
{
  "question": "Help with transitions",
  "child_name": "Alex",
  "include_image": false
}
```

---

## Error Handling

All APIs return consistent error format:

```python
{
    'success': False,
    'error': 'Error description here',
    ...other context...
}
```

**Best Practice:**
```python
result = agent.some_method()

if result['success']:
    # Process result
    data = result['data']
else:
    # Handle error
    print(f"Error: {result['error']}")
```

---

## Rate Limits

| Service | Limit | Cost When Exceeded |
|---------|-------|-------------------|
| Groq API | 14,400 req/day | Free tier limit |
| MongoDB | 512MB storage | Upgrade to M2 |
| Local SD | Unlimited | Free forever |
| Local Embeddings | Unlimited | Free forever |

---

## Response Times

| Operation | Average | Max |
|-----------|---------|-----|
| RAG Search | 0.04s | 0.5s |
| Simplification | 0.26s | 3s |
| Social Story | 0.54s | 5s |
| Image Gen (CPU) | 50s | 90s |
| Full Orchestration | 8s | 30s |

---

## Best Practices

### 1. Use Appropriate top_k
```python
# Quick search
retriever.retrieve(query, top_k=3)

# Comprehensive search
retriever.retrieve(query, top_k=10)
```

### 2. Batch Operations
```python
# More efficient
texts = ["text1", "text2", "text3"]
results = adapter.simplify_multiple(texts)

# Less efficient
for text in texts:
    result = adapter.simplify_text(text)
```

### 3. Cache Results
```python
# Cache expensive operations
@lru_cache(maxsize=100)
def get_simplified(text):
    return adapter.simplify_text(text)
```

### 4. Skip Images in Development
```python
# Faster testing
results = orch.process_question(
    question="test",
    generate_image=False  # Skip slow image generation
)
```

---

## Code Examples

### Complete Workflow
```python
from agents.orchestrator import Orchestrator

# Initialize
orch = Orchestrator()

# Process question
results = orch.process_question(
    question="How can I support my autistic child at school?",
    generate_image=False,
    generate_social_story=True,
    child_name="Jamie"
)

# Generate PDF
pdf = orch.generate_pdf_report(results)

print(f"Report: {pdf['pdf_path']}")
```

### Custom Pipeline
```python
from agents.rag_retriever import RAGRetriever
from agents.content_adapter import ContentAdapter

# Search
retriever = RAGRetriever()
search_result = retriever.retrieve("autism interventions", top_k=5)

# Get context
context = "\n".join([r['text'] for r in search_result['results']])

# Simplify
adapter = ContentAdapter()
simple = adapter.simplify_text(context[:500])

print(simple['simplified_text'])
```

---

For more examples, see the `scripts/` directory!
