# MCP Server Setup Guide

## 📋 What is MCP?

**Model Context Protocol (MCP)** lets Claude Desktop use your custom tools directly. This means you can ask Claude questions about autism and it will use your RAG system, simplify content, generate images, etc.

---

## 🚀 Setup Steps

### Step 1: Test MCP Tools

First, verify all tools work:

```bash
python scripts/test_mcp_tools.py
```

Expected output:
```
✅ PASS: search_autism_knowledge
✅ PASS: simplify_content
✅ PASS: generate_social_story
✅ PASS: generate_educational_image
✅ PASS: answer_question
✅ PASS: create_full_report

🎉 ALL MCP TOOLS WORKING!
```

---

### Step 2: Install MCP Package

```bash
pip install mcp
```

---

### Step 3: Configure Claude Desktop

#### On Mac:

1. **Find Claude Desktop config file:**
   ```bash
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "spectrum-bridge-ai": {
         "command": "python",
         "args": [
           "/Users/saranyajs/Documents/Spectrum_Bridge/SpectrumBridge-AI/mcp_server/server.py"
         ],
         "env": {
           "PYTHONPATH": "/Users/saranyajs/Documents/Spectrum_Bridge/SpectrumBridge-AI"
         }
       }
     }
   }
   ```

3. **Save the file**

4. **Restart Claude Desktop**

---

### Step 4: Test in Claude Desktop

Open Claude Desktop and try these prompts:

```
"Search my autism knowledge base for information about early signs"

"Simplify this text to Grade 2: Autism is a neurodevelopmental condition..."

"Generate a social story about going to the dentist for a child named Maya"

"Create a full autism education report about sensory processing"
```

Claude will now have access to all 6 tools!

---

## 🔧 Troubleshooting

### Issue: Tools not showing in Claude

**Solution:**
1. Check config file location is correct
2. Restart Claude Desktop completely (quit and reopen)
3. Check logs: `~/Library/Logs/Claude/mcp.log`

### Issue: Python path errors

**Solution:**
Update the `PYTHONPATH` in config to your actual project path:
```json
"env": {
  "PYTHONPATH": "/Users/saranyajs/Documents/Spectrum_Bridge/SpectrumBridge-AI"
}
```

### Issue: Virtual environment

**Solution:**
If using venv, update command to use venv python:
```json
"command": "/Users/saranyajs/Documents/Spectrum_Bridge/SpectrumBridge-AI/venv/bin/python"
```

---

## 📚 Available MCP Tools

### 1. `search_autism_knowledge`
**What it does:** Searches 4,275 autism documents
**Input:** query, top_k
**Example:** "Search for information about autism diagnosis"

### 2. `simplify_content`
**What it does:** Simplifies text to Grade 2
**Input:** text, context
**Example:** "Simplify this paragraph for a 7-year-old"

### 3. `generate_social_story`
**What it does:** Creates Carol Gray framework social stories
**Input:** situation, child_name, reading_level
**Example:** "Create a social story about waiting in line for Emma"

### 4. `generate_educational_image`
**What it does:** Generates AI images (takes ~45s)
**Input:** prompt
**Example:** "Generate an image of a child with autism playing"

### 5. `answer_question`
**What it does:** Full RAG Q&A with sources
**Input:** question, simplify
**Example:** "Answer: What are effective autism interventions?"

### 6. `create_full_report`
**What it does:** Runs orchestrator, generates PDF
**Input:** question, child_name, include_image
**Example:** "Create a full report about sensory processing for Maya"

---

## 🧪 Testing Workflow

### 1. Test Locally First
```bash
# Test all tools
python scripts/test_mcp_tools.py

# Should see 6/6 passing
```

### 2. Test MCP Server Directly
```bash
# Run server
python mcp_server/server.py
```

Should start and wait for input (Ctrl+C to stop).

### 3. Test in Claude Desktop
- Restart Claude Desktop
- Tools should appear in Claude's tool list
- Try the example prompts above

---

## ✅ Success Criteria

After setup, you should be able to:

✅ Ask Claude to search your autism knowledge base
✅ Ask Claude to simplify complex autism information  
✅ Ask Claude to create social stories
✅ Ask Claude to generate educational images
✅ Ask Claude to create full PDF reports

All using your local AI agents!

---

## 📝 Quick Reference

**Config file location (Mac):**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Server file:**
```
/Users/saranyajs/Documents/Spectrum_Bridge/SpectrumBridge-AI/mcp_server/server.py
```

**Test tools:**
```bash
python scripts/test_mcp_tools.py
```

---

## 🎯 Next Steps

1. ✅ Test tools locally
2. ✅ Configure Claude Desktop
3. ✅ Restart Claude
4. ✅ Test integration
5. ✅ Verify end-to-end flow
