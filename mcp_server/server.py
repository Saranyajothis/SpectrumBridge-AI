"""
MCP Server for Spectrum Bridge AI
Completely silent initialization for MCP protocol
"""

import sys
from pathlib import Path
import asyncio
import os
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types

# Suppress ALL output during imports and initialization
devnull = StringIO()

with redirect_stdout(devnull), redirect_stderr(devnull):
    from agents.rag_retriever import RAGRetriever
    from agents.content_adapter import ContentAdapter
    from agents.social_story_agent import SocialStoryAgent
    from agents.visual_generator import VisualGenerator
    from agents.orchestrator import Orchestrator
    
    # Initialize agents (all output suppressed)
    rag_retriever = RAGRetriever()
    content_adapter = ContentAdapter()
    social_story_agent = SocialStoryAgent()
    visual_generator = VisualGenerator()
    orchestrator = Orchestrator()

# Initialize server
server = Server("spectrum-bridge-ai")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available MCP tools"""
    return [
        types.Tool(
            name="search_autism_knowledge",
            description="Search the autism knowledge base (4,275 documents) for relevant information",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "top_k": {"type": "number", "description": "Number of results", "default": 5}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="simplify_content",
            description="Simplify text to Grade 2 reading level",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to simplify"}
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="generate_social_story",
            description="Create autism-friendly social story",
            inputSchema={
                "type": "object",
                "properties": {
                    "situation": {"type": "string", "description": "Situation to explain"},
                    "child_name": {"type": "string", "default": "I"}
                },
                "required": ["situation"]
            }
        ),
        types.Tool(
            name="generate_educational_image",
            description="Generate autism education image (45-60s)",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Image description"}
                },
                "required": ["prompt"]
            }
        ),
        types.Tool(
            name="answer_question",
            description="Answer autism question using RAG",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "simplify": {"type": "boolean", "default": False}
                },
                "required": ["question"]
            }
        ),
        types.Tool(
            name="create_full_report",
            description="Create complete report with PDF",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "child_name": {"type": "string", "default": "the child"},
                    "include_image": {"type": "boolean", "default": False}
                },
                "required": ["question"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool execution - all output suppressed"""
    
    # Suppress output during tool execution too
    with redirect_stdout(devnull), redirect_stderr(devnull):
        
        if name == "search_autism_knowledge":
            query = arguments.get("query", "")
            top_k = arguments.get("top_k", 5)
            result = rag_retriever.retrieve(query, top_k=top_k)
            
            if result['success']:
                response = f"Found {result['count']} documents:\n\n"
                for i, doc in enumerate(result['results'], 1):
                    response += f"{i}. {doc['source']} (Score: {doc['score']:.4f})\n{doc['text'][:150]}...\n\n"
                return [types.TextContent(type="text", text=response)]
            return [types.TextContent(type="text", text="No results found")]
        
        elif name == "simplify_content":
            text = arguments.get("text", "")
            result = content_adapter.simplify_text(text)
            
            if result['success']:
                return [types.TextContent(type="text", text=result['simplified_text'])]
            return [types.TextContent(type="text", text="Simplification failed")]
        
        elif name == "generate_social_story":
            situation = arguments.get("situation", "")
            child_name = arguments.get("child_name", "I")
            result = social_story_agent.generate_social_story(situation, child_name)
            
            if result['success']:
                response = f"{result['title']}\n\n{result['story']}"
                return [types.TextContent(type="text", text=response)]
            return [types.TextContent(type="text", text="Story generation failed")]
        
        elif name == "generate_educational_image":
            prompt = arguments.get("prompt", "")
            result = visual_generator.generate_image(prompt)
            
            response = f"Image: {result['filename']}\nPath: {result['image_path']}"
            return [types.TextContent(type="text", text=response)]
        
        elif name == "answer_question":
            question = arguments.get("question", "")
            simplify = arguments.get("simplify", False)
            
            rag_result = rag_retriever.retrieve(question, top_k=5)
            if rag_result['count'] == 0:
                return [types.TextContent(type="text", text="No information found")]
            
            context = "\n".join([r['text'] for r in rag_result['results']])
            response = context[:500]
            
            if simplify:
                simp = content_adapter.simplify_text(response)
                if simp['success']:
                    response = simp['simplified_text']
            
            return [types.TextContent(type="text", text=response)]
        
        elif name == "create_full_report":
            question = arguments.get("question", "")
            child_name = arguments.get("child_name", "the child")
            include_image = arguments.get("include_image", False)
            
            results = orchestrator.process_question(question, include_image, True, child_name)
            pdf = orchestrator.generate_pdf_report(results)
            
            response = f"Report created!\nPDF: {pdf['pdf_path'] if pdf['success'] else 'Failed'}"
            return [types.TextContent(type="text", text=response)]
    
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="spectrum-bridge-ai",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
