"""Code Generation Routes - Generate SDK wrapper code from analysis results."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.sdk_generator import SDKGenerator
from services.history_service import HistoryService

router = APIRouter(tags=["generation"])
generator = SDKGenerator()
history_service = HistoryService()


class GenerateSdkRequest(BaseModel):
    """Request to generate SDK code."""
    language: str  # python, javascript, typescript, go, java
    endpoints: List[Dict]
    api_name: str = "API"
    auth_method: Optional[str] = None


class GenerateTestsRequest(BaseModel):
    """Request to generate test suite."""
    language: str
    endpoints: List[Dict]
    api_name: str = "API"


@router.post("/generate-sdk")
async def generate_sdk(request: GenerateSdkRequest):
    """Generate SDK wrapper code for specified language.
    
    Args:
        language: Target language (python, javascript, typescript, go, java)
        endpoints: List of extracted endpoints
        api_name: Name of the API
        auth_method: Authentication method used
    
    Returns:
        Generated SDK code and metadata
    """
    try:
        if request.language not in ['python', 'javascript', 'typescript', 'go', 'java']:
            raise ValueError(f"Unsupported language: {request.language}")
        
        code = generator.generate_sdk(
            request.language,
            request.endpoints,
            request.api_name
        )
        
        # Save to history
        try:
            generation_id = history_service.save_generation(
                analysis_id="latest",
                language=request.language,
                code=code,
                api_name=request.api_name
            )
        except Exception as e:
            print(f"Warning: Could not save generation to history: {e}")
            generation_id = None
        
        return {
            "status": "success",
            "language": request.language,
            "api_name": request.api_name,
            "endpoint_count": len(request.endpoints),
            "code": code,
            "code_length": len(code),
            "generation_id": generation_id,
            "features": [
                "Async/await support",
                "Error handling",
                "Type hints" if request.language in ['python', 'typescript', 'java'] else None,
                f"Authentication: {request.auth_method}" if request.auth_method else None,
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-tests")
async def generate_tests(request: GenerateTestsRequest):
    """Generate test suite for SDK.
    
    Args:
        language: Target language
        endpoints: List of endpoints
        api_name: Name of the API
    
    Returns:
        Generated test code
    """
    try:
        if request.language not in ['python', 'javascript', 'typescript']:
            raise HTTPException(
                status_code=400,
                detail=f"Test generation not supported for {request.language}"
            )
        
        code = generator.generate_test_suite(
            request.language,
            request.endpoints,
            request.api_name
        )
        
        return {
            "status": "success",
            "language": request.language,
            "test_type": "unit",
            "code": code,
            "code_length": len(code),
            "test_cases": [
                "Client initialization",
                "Successful requests",
                "Error handling",
                "Request validation",
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages for code generation."""
    return {
        "languages": [
            {
                "name": "Python",
                "id": "python",
                "icon": "🐍",
                "features": ["Async support", "Type hints", "Error handling"]
            },
            {
                "name": "JavaScript",
                "id": "javascript",
                "icon": "🟨",
                "features": ["Promise-based", "Error handling", "Node.js compatible"]
            },
            {
                "name": "TypeScript",
                "id": "typescript",
                "icon": "🔷",
                "features": ["Full type safety", "Generic types", "Interfaces"]
            },
            {
                "name": "Go",
                "id": "go",
                "icon": "🐹",
                "features": ["Goroutines", "Error handling", "Efficient"]
            },
            {
                "name": "Java",
                "id": "java",
                "icon": "☕",
                "features": ["Full OOP", "Strong typing", "Enterprise ready"]
            },
        ]
    }
