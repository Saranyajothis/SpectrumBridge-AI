# 🌟 Spectrum Bridge AI

**AI-Powered Autism Education Platform with FREE APIs**

A comprehensive system that helps parents, teachers, and caregivers understand and support children with autism using AI-powered tools - all completely free.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Coverage](https://img.shields.io/badge/coverage-95.5%25-brightgreen.svg)]()
[![Cost](https://img.shields.io/badge/cost-$0%2Fmonth-success.svg)]()

---

## 🎯 Features

### 🔍 **RAG-Powered Knowledge Base**
- Search across 4,275+ autism research documents
- Vector similarity search with MongoDB
- Instant, relevant information retrieval

### 📝 **Grade 2 Content Simplification**
- Simplifies complex autism information to Grade 2 reading level
- Perfect for young children (7-8 years old)
- Verified readability metrics

### 📖 **Social Story Generator**
- Creates autism-friendly social stories
- Follows Carol Gray's framework
- Personalized for each child

### 🎨 **Educational Image Generation**
- AI-generated autism education images
- Local Stable Diffusion (no API costs)
- Professional quality illustrations

### 🤖 **Intelligent Orchestrator**
- Coordinates all agents seamlessly
- Parallel execution for speed
- Generates comprehensive PDF reports

### 🔌 **Claude Desktop Integration (MCP)**
- 6 custom tools for Claude
- Natural language interface
- Seamless AI assistance

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- MongoDB Atlas account (free tier)
- 8GB RAM minimum
- 10GB disk space

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/SpectrumBridge-AI.git
cd SpectrumBridge-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create a `.env` file with:

```env
# Required
MONGODB_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key

# Optional
HF_TOKEN=your_huggingface_token
GEMINI_API_KEY=your_gemini_key  # Backup LLM
```

### Initial Setup

```bash
# 1. Add PDFs to knowledge_base/pdfs/
# 2. Generate embeddings
python scripts/03_generate_embeddings.py

# 3. Upload to MongoDB
python scripts/04_upload_to_mongodb.py

# 4. Test the system
python scripts/test_all_agents.py
```

---

## 📚 Usage

### Command Line

#### Search Knowledge Base
```bash
python -c "
from agents.rag_retriever import RAGRetriever
retriever = RAGRetriever()
result = retriever.retrieve('early signs of autism', top_k=5)
print(result)
"
```

#### Simplify Text
```bash
python -c "
from agents.content_adapter import ContentAdapter
adapter = ContentAdapter()
result = adapter.simplify_text('Autism Spectrum Disorder is...')
print(result['simplified_text'])
"
```

#### Generate Social Story
```bash
python -c "
from agents.social_story_agent import SocialStoryAgent
agent = SocialStoryAgent()
story = agent.generate_social_story('going to the doctor', 'Emma')
print(story['title'])
print(story['story'])
"
```

#### Create Full Report
```bash
python agents/orchestrator.py
```

### Claude Desktop (MCP Integration)

After setting up MCP (see [MCP Setup Guide](mcp_server/MCP_SETUP_GUIDE.md)):

```
"Search my autism knowledge base for information about sensory processing"

"Simplify this to Grade 2: [your complex text]"

"Create a social story about waiting in line for a child named Alex"

"Generate a full report about communication strategies"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         User Interface Layer             │
│  (CLI / MCP / API / Web Dashboard)      │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Orchestrator Layer               │
│   (Coordinates all agents in parallel)  │
└─────────────────────────────────────────┘
                  ↓
┌───────────────────────────────────────────────────────┐
│                 Agent Layer (5 Agents)                 │
├───────────────────────────────────────────────────────┤
│  1. RAG Retriever    → Vector search & retrieval      │
│  2. Content Adapter  → Grade 2 simplification         │
│  3. Social Story     → Structured story creation      │
│  4. Visual Generator → Image generation               │
│  5. Orchestrator     → Multi-agent coordination       │
└───────────────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Data Layer                      │
│  • MongoDB Vector DB (4,275+ docs)      │
│  • Local embeddings (384-dim)           │
│  • PDF knowledge base                    │
└─────────────────────────────────────────┘
```

---

## 💰 Cost Breakdown

| Component | Service | Monthly Cost | Limits |
|-----------|---------|--------------|--------|
| Vector Database | MongoDB M0 | **$0** | 512MB storage |
| Embeddings | Local (sentence-transformers) | **$0** | Unlimited |
| LLM (Groq) | Llama 3.3 70B | **$0** | 14,400 req/day |
| Image Generation | Local Stable Diffusion | **$0** | Unlimited |
| **TOTAL** | - | **$0/month** | - |

---

## 📊 Performance Metrics

- **RAG Retrieval:** 0.043s average
- **Content Simplification:** 0.263s average
- **Social Story Generation:** 0.535s average
- **Full Orchestration:** 0.64s (without images)
- **Image Generation:** 45-60s (local CPU)
- **Test Coverage:** 95.5%

---

## 🧪 Testing

### Run All Tests
```bash
# Test individual agents
python scripts/test_all_agents.py

# Test content adapter
python scripts/test_content_adapter.py

# Test orchestrator
python scripts/test_orchestrator.py

# Comprehensive test suite
python scripts/comprehensive_test_suite.py

# Unit tests with coverage
pytest tests/ -v --cov=agents --cov-report=html
```

### Sample Lessons
The system includes 5 real-world sample lessons:
1. Understanding Early Signs of Autism
2. Sensory Processing Support
3. Communication Strategies
4. School Transitions
5. Complete Education Package

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t spectrum-bridge-ai .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### Environment Setup

Create `.env` file before running:
```bash
cp .env.example .env
# Edit .env with your credentials
```

---

## 📁 Project Structure

```
SpectrumBridge-AI/
├── agents/                      # 5 AI Agents
│   ├── rag_retriever.py        # Vector search
│   ├── content_adapter.py      # Grade 2 simplification
│   ├── social_story_agent.py   # Social stories
│   ├── visual_generator.py     # Image generation
│   └── orchestrator.py         # Multi-agent coordination
│
├── knowledge_base/              # Data storage
│   ├── pdfs/                   # Source documents
│   └── embeddings/             # Generated embeddings
│
├── scripts/                     # Utility scripts
│   ├── 01_collect_autism_pdfs.py
│   ├── 02_download_embedding_model.py
│   ├── 03_generate_embeddings.py
│   ├── 04_upload_to_mongodb.py
│   ├── test_all_agents.py
│   ├── test_orchestrator.py
│   └── comprehensive_test_suite.py
│
├── tests/                       # Unit tests
│   ├── test_content_adapter_unit.py
│   └── test_agents_integration.py
│
├── mcp_server/                  # Claude Desktop integration
│   ├── server.py
│   └── MCP_SETUP_GUIDE.md
│
├── output/                      # Generated outputs
│   ├── generated_images/
│   └── *.pdf
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔧 Configuration

### MongoDB Atlas Setup

1. Create free M0 cluster at https://cloud.mongodb.com
2. Create database: `spectrum_bridge_AI`
3. Create collection: `knowledge_base`
4. Create vector search index:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    }
  ]
}
```

### Groq API Setup

1. Sign up at https://console.groq.com
2. Create API key
3. Add to `.env` file
4. Free tier: 14,400 requests/day

---

## 🎓 Use Cases

### For Parents
- Get simplified explanations of autism concepts
- Create personalized social stories for daily situations
- Access research-backed information easily
- Generate visual learning aids

### For Teachers
- Prepare autism-friendly lesson materials
- Create individualized education plans
- Access evidence-based strategies
- Generate classroom visual supports

### For Therapists
- Quick reference to intervention strategies
- Create client-specific social narratives
- Access latest research efficiently
- Generate session materials

---

## 🔌 MCP Integration (Claude Desktop)

Enable your Spectrum Bridge AI tools in Claude Desktop:

1. Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add configuration (see [MCP Setup Guide](mcp_server/MCP_SETUP_GUIDE.md))
3. Restart Claude Desktop
4. Use natural language to access all tools

Example:
```
"Search my autism knowledge base for sensory processing strategies"
"Create a social story about transitions for Maya"
"Simplify this medical text to Grade 2 level"
```

---

## 📈 Roadmap

### Completed ✅
- [x] RAG system with vector database
- [x] Content simplification to Grade 2
- [x] Social story generation
- [x] Local image generation
- [x] Multi-agent orchestration
- [x] MCP server for Claude Desktop
- [x] Comprehensive testing (95.5% coverage)
- [x] Docker containerization

### Future Enhancements 🚀
- [ ] Web dashboard UI
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Voice interaction
- [ ] Collaborative features for teams
- [ ] Analytics and insights
- [ ] Custom fine-tuned models

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### APIs & Services (All FREE)
- **Groq** - Lightning-fast LLM inference
- **MongoDB Atlas** - Vector database (M0 free tier)
- **HuggingFace** - Model hosting and transformers
- **Sentence Transformers** - Local embedding generation
- **Stable Diffusion** - Local image generation

### Research & Frameworks
- **Carol Gray** - Social Stories framework
- **CDC** - Autism screening and diagnosis guidelines
- **NAC** - Evidence-based practices

---

## 📞 Support

- **Documentation:** See `docs/` folder
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions about autism or any medical condition.

---

## 🌟 Star Us!

If you find this project helpful, please ⭐ star the repository!

---

## 📊 Stats

- **Test Coverage:** 95.5%
- **Documents Indexed:** 4,275+
- **Agents:** 5 independent AI agents
- **MCP Tools:** 6 Claude Desktop tools
- **Monthly Cost:** $0
- **Languages:** Python
- **Lines of Code:** 5,000+

---

**Built with ❤️ for the autism community**
