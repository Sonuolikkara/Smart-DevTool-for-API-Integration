"""
Document Management Routes
- Upload documents
- Fetch from URLs
- Manage document storage
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict
import shutil
from pathlib import Path

from services.doc_processor import (
    fetch_documentation,
    parse_html_docs,
    chunk_documentation,
    extract_headers
)

router = APIRouter()

# Pydantic models
class FetchDocumentRequest(BaseModel):
    url: str

# Store uploaded files temporarily
UPLOAD_DIR = Path("./uploaded_docs")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> Dict:
    """
    Upload API documentation file
    Supports: PDF, TXT, MD, HTML
    """
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.txt', '.md', '.html', '.json'}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. Use: {', '.join(allowed_extensions)}"
            )
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read and parse content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse based on file type
        if file_ext == '.html':
            parsed_content = parse_html_docs(content)
        else:
            parsed_content = content
        
        # Extract headers
        headers = extract_headers(parsed_content)
        
        # Create chunks
        chunks = chunk_documentation(parsed_content)
        
        return {
            "status": "success",
            "message": f"Document '{file.filename}' uploaded successfully",
            "file_name": file.filename,
            "file_size": file.size,
            "content_preview": parsed_content[:200],
            "headers_found": len(headers),
            "chunks_created": len(chunks),
            "file_path": str(file_path)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading document: {str(e)}"
        )


@router.post("/fetch")
async def fetch_documentation_from_url(request: FetchDocumentRequest) -> Dict:
    """
    Fetch API documentation from URL
    Example: https://docs.github.com/en/rest
    """
    try:
        url = request.url
        
        if not url.startswith(('http://', 'https://')):
            raise HTTPException(
                status_code=400,
                detail="URL must start with http:// or https://"
            )
        
        # Fetch documentation
        html_content = await fetch_documentation(url)
        
        # Parse HTML
        parsed_content = parse_html_docs(html_content)
        
        # Extract headers
        headers = extract_headers(parsed_content)
        
        # Create chunks
        chunks = chunk_documentation(parsed_content)
        
        return {
            "status": "success",
            "message": f"Documentation fetched from {url}",
            "url": url,
            "content_length": len(parsed_content),
            "content_preview": parsed_content[:300],
            "headers_found": len(headers),
            "chunks_created": len(chunks),
            "top_headers": [h for h in headers[:5]]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching documentation: {str(e)}"
        )


@router.get("/uploaded")
async def list_uploaded_documents() -> Dict:
    """
    List all uploaded documents
    """
    try:
        files = list(UPLOAD_DIR.glob("*"))
        
        documents = []
        for file in files:
            documents.append({
                "name": file.name,
                "size": file.stat().st_size,
                "created": file.stat().st_ctime,
                "type": file.suffix
            })
        
        return {
            "status": "success",
            "total_documents": len(documents),
            "documents": documents
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )


@router.delete("/uploaded/{document_name}")
async def delete_document(document_name: str) -> Dict:
    """
    Delete an uploaded document
    """
    try:
        file_path = UPLOAD_DIR / document_name
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Document '{document_name}' not found"
            )
        
        file_path.unlink()
        
        return {
            "status": "success",
            "message": f"Document '{document_name}' deleted"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )
