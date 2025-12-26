# 🎬 Demo Video Script

## Video Length: 5-7 minutes

---

## 🎯 Opening (30 seconds)

**[Screen: Project Title Slide]**

"Hi! I'm excited to show you Spectrum Bridge AI - an AI-powered platform that makes autism education accessible to everyone, completely free."

**Key Points:**
- Built in 3 weeks
- 5 AI agents
- $0 monthly cost
- 95.5% test coverage

---

## 📚 Part 1: The Problem (45 seconds)

**[Screen: Show complex autism research paper]**

"Parents and teachers face three major challenges:

1. Autism research is written in complex medical language
2. Creating individualized materials takes hours
3. Professional tools cost hundreds of dollars per month

Spectrum Bridge AI solves all three."

---

## 🔍 Part 2: RAG System Demo (1 minute)

**[Screen: Terminal running test_vector_search.py]**

```bash
python scripts/test_vector_search.py
```

**Demonstrate:**
1. Search: "early signs of autism"
2. Show: 5 results with relevance scores (0.84+)
3. Highlight: 4,275 documents, instant search

**Narration:**
"Our RAG system searches 4,275 autism research documents instantly. Notice the high relevance scores - 0.84 to 0.85 - meaning highly accurate results."

---

## 📝 Part 3: Content Simplification Demo (1 minute)

**[Screen: Run content adapter test]**

```bash
python agents/content_adapter.py
```

**Show:**
- Input: Complex medical text
- Output: Grade 2 simplified version
- Metrics: 4 words/sentence, Grade 1-2 level

**Narration:**
"Watch as we transform complex autism terminology into simple language a 7-year-old can understand. The system verifies it meets Grade 2 readability standards."

---

## 📖 Part 4: Social Story Demo (1 minute)

**[Screen: Run social story agent]**

```bash
python agents/social_story_agent.py
```

**Show:**
- Generate story: "going to the doctor" for "Emma"
- Display: Title + structured story
- Highlight: Carol Gray framework compliance

**Narration:**
"Social stories help autistic children understand new situations. Our AI generates personalized stories following the evidence-based Carol Gray framework in seconds."

---

## 🎨 Part 5: Image Generation Demo (1 minute)

**[Screen: Show image being generated]**

```bash
python agents/visual_generator.py
```

**Show:**
- Prompt: "child with autism in classroom"
- Generation process
- Final image

**Narration:**
"The system generates educational images locally using Stable Diffusion. No API costs, completely free and unlimited."

---

## 🤖 Part 6: Full Orchestration Demo (1.5 minutes)

**[Screen: Run orchestrator]**

```bash
python agents/orchestrator.py
```

**Demonstrate:**
1. Input: "How can I help my child with sensory processing?"
2. Show parallel execution:
   - RAG retrieval
   - Content simplification
   - Social story generation
3. Show PDF report generated
4. Highlight: <1 second total time

**Narration:**
"The orchestrator coordinates all agents in parallel. Watch as it retrieves information, simplifies it, creates a social story, and generates a professional PDF report - all in under one second."

---

## 🔌 Part 7: Claude Desktop Integration (1 minute)

**[Screen: Claude Desktop with MCP tools]**

**Demonstrate:**
1. Ask Claude: "Search my autism knowledge base for communication strategies"
2. Show Claude using your custom tools
3. Ask: "Create a social story about waiting in line for Alex"
4. Show instant, personalized result

**Narration:**
"Through MCP integration, you can use natural language in Claude Desktop to access all these tools. No coding required - just ask Claude."

---

## 📊 Part 8: System Overview (45 seconds)

**[Screen: Architecture diagram or stats]**

**Show:**
- 5 AI Agents
- 4,275+ documents
- 95.5% test coverage
- $0/month cost
- 6 MCP tools

**Narration:**
"The complete system includes 5 independent AI agents, comprehensive testing with 95.5% coverage, and costs absolutely nothing to run. All APIs are free tier."

---

## 🎯 Part 9: Impact & Closing (30 seconds)

**[Screen: Use cases/benefits slide]**

"Spectrum Bridge AI empowers:
- Parents to understand their child's diagnosis
- Teachers to create individualized materials
- Therapists to access research quickly

All for free. All powered by AI.

The code is open source and available on GitHub."

**[Screen: GitHub link + Thank you slide]**

"Thank you for watching! Star the repo if you find it useful!"

---

## 📋 Demo Checklist

Before recording:

- [ ] All tests passing
- [ ] Clean terminal (clear history)
- [ ] Sample data loaded
- [ ] Services running
- [ ] Screen recording software ready
- [ ] Microphone tested
- [ ] Script practiced

---

## 🎥 Recording Tips

### Setup
- Use screen recording software (OBS, QuickTime, Loom)
- 1080p resolution minimum
- Clear, simple terminal theme
- Large font size (18-20pt)

### Narration
- Speak clearly and slowly
- Pause between sections
- Emphasize key metrics
- Show, don't just tell

### Editing
- Add title cards between sections
- Highlight important text
- Speed up slow operations (image generation)
- Add background music (optional, keep subtle)

---

## 📤 Publishing

### Upload To:
- YouTube (public or unlisted)
- Loom (for embedding)
- LinkedIn
- Portfolio website

### Include:
- GitHub link in description
- Timestamps for each section
- Links to documentation
- Contact information

---

## 🎬 Alternative: Quick Demo (2 minutes)

For a shorter version:

1. Show architecture diagram (15s)
2. Run comprehensive test suite (30s)
3. Show MCP integration in Claude (45s)
4. Show final stats (30s)

**Script:**
```bash
# One command demo
python scripts/comprehensive_test_suite.py
```

Shows everything at once: all agents, all tests, all metrics.

---

**Ready to record your demo!** 🎥
