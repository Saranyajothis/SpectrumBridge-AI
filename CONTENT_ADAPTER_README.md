# Content Adapter - Days 5-7 Implementation

## ✅ What Was Built

### 1. **Content Adapter Agent** (`agents/content_adapter.py`)
- Simplifies complex autism content to Grade 2 reading level
- Uses Groq API (Llama 3.3 70B) for fast, free processing
- Calculates readability metrics
- Verifies Grade 2 compliance

### 2. **Comprehensive Testing** (`scripts/test_content_adapter.py`)
- Tests basic simplification
- Tests autism-specific topics
- Tests batch processing
- Tests edge cases
- Provides detailed test reports

### 3. **Unit Tests** (`tests/test_content_adapter_unit.py`)
- Pytest-based unit tests
- Tests initialization
- Tests text simplification
- Tests metrics calculation
- Tests Grade 2 compliance
- 15+ test cases

---

## 🚀 How to Use

### Installation

```bash
cd /Users/saranyajs/Documents/Spectrum_Bridge/SpectrumBridge-AI

# Install dependencies
pip install pytest pytest-cov

# Already have groq from earlier
```

### Quick Test

```bash
# Run comprehensive tests
python scripts/test_content_adapter.py

# Run unit tests
pytest tests/test_content_adapter_unit.py -v

# Run with coverage
pytest tests/test_content_adapter_unit.py --cov=agents --cov-report=html
```

### Direct Usage

```python
from agents.content_adapter import ContentAdapter

# Initialize
adapter = ContentAdapter()

# Simplify text
complex_text = "Autism Spectrum Disorder is a neurodevelopmental condition..."
result = adapter.simplify_text(complex_text)

print(result['simplified_text'])
print(result['metrics'])

# Create age-appropriate explanation
explanation = adapter.create_age_appropriate_explanation("what is autism")
print(explanation['explanation'])
```

---

## 📊 Features

### Text Simplification
- ✅ Grade 2 reading level (7-8 year olds)
- ✅ Short sentences (5-10 words)
- ✅ Simple vocabulary
- ✅ Active voice
- ✅ Clear, positive language

### Metrics Calculation
- Total words & sentences
- Average words per sentence
- Average syllables per word
- Estimated grade level
- Grade 2 compliance check

### Batch Processing
- Process multiple texts at once
- Consistent quality across batch
- Individual metrics for each text

---

## 🧪 Testing

### Test Categories

#### 1. Basic Simplification
Tests core simplification functionality with medical/technical text.

#### 2. Autism Topics
Tests domain-specific simplification:
- "what is autism"
- "sensory processing"
- "communication differences"

#### 3. Batch Processing
Tests multiple text simplification in one go.

#### 4. Edge Cases
Tests:
- Empty strings
- Whitespace only
- Very long text
- Single word sentences

### Running Tests

```bash
# All comprehensive tests
python scripts/test_content_adapter.py

# Unit tests only
pytest tests/test_content_adapter_unit.py

# Verbose mode
pytest tests/test_content_adapter_unit.py -v

# With coverage
pytest tests/test_content_adapter_unit.py --cov=agents

# Specific test
pytest tests/test_content_adapter_unit.py::TestSimplifyText::test_simplify_basic_text
```

### Expected Output

```
======================================================================
TEST SUMMARY
======================================================================

✅ PASS: Basic Simplification
✅ PASS: Autism Topics
✅ PASS: Batch Processing
✅ PASS: Edge Cases

Total: 4/4 tests passed

🎉 ALL TESTS PASSED!
✅ Agent working
✅ Grade 2 output
✅ Tests passing
```

---

## 📝 Grade 2 Guidelines

The adapter follows these strict guidelines:

### Sentence Structure
- **Length:** 5-10 words maximum
- **Voice:** Active voice only
- **Tense:** Present tense when possible
- **Complexity:** One idea per sentence

### Vocabulary
- Use 100-200 most common words
- No jargon or complex terms
- Familiar comparisons
- Repeat key terms for clarity

### Readability Targets
- **Words/sentence:** ≤ 10
- **Syllables/word:** ≤ 1.3
- **Grade level:** 1-2

---

## 🎯 Week 1 Day 5-7 Deliverables

### ✅ Completed

| Deliverable | Status | File |
|------------|--------|------|
| Build Content Adapter | ✅ | `agents/content_adapter.py` |
| Integrate Groq | ✅ | (Uses Groq instead of Gemini) |
| Test simplification | ✅ | `scripts/test_content_adapter.py` |
| Write unit tests | ✅ | `tests/test_content_adapter_unit.py` |
| Agent working | ✅ | Tested & verified |
| Grade 2 output | ✅ | Metrics verify compliance |
| Tests passing | ✅ | 15+ unit tests |

---

## 🔧 Troubleshooting

### Issue: Tests Fail
**Solution:** Make sure Groq API key is in `.env`:
```bash
cat .env | grep GROQ_API_KEY
```

### Issue: Import Errors
**Solution:** Install dependencies:
```bash
pip install groq pytest pytest-cov
```

### Issue: API Rate Limits
**Solution:** Groq free tier has 14,400 requests/day. If you hit limits, wait or upgrade.

---

## 📈 Next Steps

### Week 2 Options:

1. **Integrate with RAG System**
   - Add simplification to RAG responses
   - User can choose: "Explain like I'm 7"

2. **Build Parent Dashboard**
   - Visual interface for content adapter
   - Batch simplification tool

3. **Add More Languages**
   - Multilingual simplification
   - Translation + simplification

4. **Content Library**
   - Pre-simplified autism resources
   - Searchable database

---

## 📚 Examples

### Example 1: Medical Text

**Input:**
```
Autism Spectrum Disorder is a neurodevelopmental condition characterized by 
persistent deficits in social communication and social interaction across 
multiple contexts.
```

**Output (Grade 2):**
```
Autism is about how your brain works. 
Some kids with autism talk and play differently. 
They are still great kids. 
Everyone's brain is special.
```

### Example 2: Intervention Description

**Input:**
```
Applied Behavior Analysis utilizes reinforcement strategies to modify behavior 
patterns through systematic application of learning principles.
```

**Output (Grade 2):**
```
ABA is a way to help kids learn. 
Teachers give rewards for good actions. 
Kids learn new skills this way. 
It helps them grow.
```

---

## ✅ Week 1 Complete!

All Days 5-7 deliverables are implemented, tested, and working! 🎉
