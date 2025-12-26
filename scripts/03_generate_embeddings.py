"""
Step 3: Process PDFs and Generate Embeddings Locally
Extracts text from PDFs, chunks them, and generates embeddings
"""

import os
from pathlib import Path
from typing import List, Dict
import json
from tqdm import tqdm

from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np

# Paths
BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "knowledge_base" / "pdfs"
OUTPUT_DIR = BASE_DIR / "knowledge_base" / "embeddings"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"

# Chunking configuration
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 50  # overlap between chunks

class PDFProcessor:
    def __init__(self, model_name=MODEL_NAME):
        """Initialize the PDF processor with embedding model"""
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✓ Model loaded (dimension: {self.model.get_sentence_embedding_dimension()})")
        
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF file"""
        try:
            reader = PdfReader(str(pdf_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"✗ Error reading {pdf_path.name}: {str(e)}")
            return ""
    
    def chunk_text(self, text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[str]:
        """Split text into overlapping chunks"""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_len:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # Only break if we're not losing too much
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if len(c) > 50]  # Filter out very small chunks
    
    def process_pdf(self, pdf_path: Path) -> List[Dict]:
        """Process a single PDF: extract text, chunk, and create metadata"""
        print(f"Processing: {pdf_path.name}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return []
        
        # Chunk text
        chunks = self.chunk_text(text)
        print(f"  → Created {len(chunks)} chunks")
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "text": chunk,
                "metadata": {
                    "source": pdf_path.name,
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            }
            documents.append(doc)
        
        return documents
    
    def generate_embeddings(self, documents: List[Dict]) -> List[Dict]:
        """Generate embeddings for all documents"""
        print(f"\nGenerating embeddings for {len(documents)} chunks...")
        
        # Extract texts
        texts = [doc["text"] for doc in documents]
        
        # Generate embeddings with progress bar
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32
        )
        
        # Add embeddings to documents
        for doc, embedding in zip(documents, embeddings):
            doc["embedding"] = embedding.tolist()
        
        return documents
    
    def process_all_pdfs(self) -> List[Dict]:
        """Process all PDFs in the directory"""
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        
        if not pdf_files:
            print(f"✗ No PDF files found in {PDF_DIR}")
            return []
        
        print(f"\n{'='*60}")
        print(f"Found {len(pdf_files)} PDF files")
        print(f"{'='*60}\n")
        
        all_documents = []
        
        for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
            docs = self.process_pdf(pdf_path)
            all_documents.extend(docs)
        
        print(f"\n✓ Total chunks created: {len(all_documents)}")
        
        return all_documents
    
    def save_embeddings(self, documents: List[Dict], output_file: str = "embeddings.json"):
        """Save embeddings to file"""
        output_path = OUTPUT_DIR / output_file
        
        print(f"\nSaving embeddings to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2)
        
        # Calculate file size
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"✓ Saved {len(documents)} embeddings ({size_mb:.2f} MB)")
        
        return output_path

def main():
    print("\n" + "="*60)
    print("PDF PROCESSING & EMBEDDING GENERATION")
    print("="*60 + "\n")
    
    # Initialize processor
    processor = PDFProcessor()
    
    # Process all PDFs
    documents = processor.process_all_pdfs()
    
    if not documents:
        print("\n✗ No documents to process. Please add PDFs first.")
        return
    
    # Generate embeddings
    documents_with_embeddings = processor.generate_embeddings(documents)
    
    # Save to file
    output_path = processor.save_embeddings(documents_with_embeddings)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    # Count unique PDFs
    unique_pdfs = set(doc["metadata"]["source"] for doc in documents_with_embeddings)
    print(f"✓ Processed PDFs: {len(unique_pdfs)}")
    print(f"✓ Total chunks: {len(documents_with_embeddings)}")
    print(f"✓ Embedding dimension: {len(documents_with_embeddings[0]['embedding'])}")
    print(f"✓ Output file: {output_path}")
    
    print(f"\n{'='*60}")
    print("Next Steps:")
    print("1. Review the embeddings file")
    print("2. Proceed to Step 4: Upload to MongoDB")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
