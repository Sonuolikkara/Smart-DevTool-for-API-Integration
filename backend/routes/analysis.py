"""
API Analysis Routes
- Extract endpoints
- Detect authentication
- Analyze security
- Generate summaries
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, List
from pydantic import BaseModel

from services.api_analyzer import (
    extract_endpoints,
    extract_parameters,
    detect_auth_method,
    extract_response_format,
    analyze_endpoint_security,
    generate_endpoint_summary
)
from services.history_service import HistoryService

router = APIRouter()
history_service = HistoryService()


class AnalysisRequest(BaseModel):
    """Request model for API analysis"""
    documentation: str
    url: Optional[str] = None


@router.post("/extract-endpoints")
async def extract_endpoints_route(documentation: str) -> Dict:
    """
    Extract API endpoints from documentation text
    
    Returns endpoints with:
    - HTTP method (GET, POST, etc)
    - Path (/users, /users/{id}, etc)
    - Description
    """
    try:
        if not documentation or len(documentation) < 10:
            raise HTTPException(
                status_code=400,
                detail="Documentation text is too short (minimum 10 characters)"
            )
        
        endpoints = extract_endpoints(documentation)
        summary = generate_endpoint_summary(endpoints)
        
        return {
            "status": "success",
            "endpoints_found": len(endpoints),
            "endpoints": endpoints[:20],  # Return first 20
            "summary": summary,
            "message": f"Found {len(endpoints)} endpoints in documentation"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting endpoints: {str(e)}"
        )


@router.post("/detect-auth")
async def detect_authentication_route(documentation: str) -> Dict:
    """
    Detect authentication method from documentation
    
    Can identify:
    - Bearer Token
    - API Key
    - OAuth 2.0
    - Basic Auth
    - JWT
    - AWS Signature
    - No Auth (Public API)
    """
    try:
        if not documentation or len(documentation) < 10:
            raise HTTPException(
                status_code=400,
                detail="Documentation text is too short"
            )
        
        auth_info = detect_auth_method(documentation)
        
        return {
            "status": "success",
            "primary_auth": auth_info['primary'],
            "auth_methods": auth_info['methods'],
            "confidence": auth_info['confidence'],
            "message": f"Detected {auth_info['primary']} authentication"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting authentication: {str(e)}"
        )


@router.post("/analyze-response-format")
async def analyze_response_format_route(documentation: str) -> Dict:
    """
    Identify response format from documentation
    
    Can identify:
    - JSON
    - XML
    - HTML
    - Plain Text
    - CSV
    """
    try:
        if not documentation or len(documentation) < 10:
            raise HTTPException(
                status_code=400,
                detail="Documentation text is too short"
            )
        
        response_format = extract_response_format(documentation)
        
        return {
            "status": "success",
            "primary_format": response_format['primary'],
            "supported_formats": response_format['formats'],
            "content_types": response_format['content_types'],
            "message": f"Primary response format: {response_format['primary']}"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing response format: {str(e)}"
        )


@router.post("/analyze-security")
async def analyze_security_route(documentation: str) -> Dict:
    """
    Analyze security aspects of API
    
    Checks for:
    - Rate limiting
    - HTTPS requirement
    - Authentication requirement
    - CORS configuration
    """
    try:
        if not documentation or len(documentation) < 10:
            raise HTTPException(
                status_code=400,
                detail="Documentation text is too short"
            )
        
        security = analyze_endpoint_security(documentation)
        
        return {
            "status": "success",
            "security_analysis": security,
            "security_score": sum(security.values()) / len(security),
            "message": "Security analysis complete"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing security: {str(e)}"
        )


@router.post("/analyze-full")
async def analyze_full_route(request: AnalysisRequest) -> Dict:
    """
    Complete API analysis pipeline
    
    Performs:
    1. Endpoint extraction
    2. Parameter identification
    3. Authentication detection
    4. Response format analysis
    5. Security assessment
    6. Summary generation
    """
    try:
        documentation = request.documentation
        
        if not documentation or len(documentation) < 10:
            raise HTTPException(
                status_code=400,
                detail="Documentation text is too short"
            )
        
        # Extract endpoints
        endpoints = extract_endpoints(documentation)
        
        # Detect auth
        auth_info = detect_auth_method(documentation)
        
        # Analyze response format
        response_format = extract_response_format(documentation)
        
        # Analyze security
        security = analyze_endpoint_security(documentation)
        
        # Generate summary
        summary = generate_endpoint_summary(endpoints)
        
        # Format response for frontend
        response_data = {
            "status": "success",
            "source": request.url or "uploaded",
            "endpoints": endpoints[:50],  # Limit to 50 endpoints for display
            "endpoints_count": len(endpoints),
            "auth_method": auth_info['primary'],
            "auth_methods": auth_info['methods'],
            "response_format": response_format['primary'],
            "all_formats": response_format['formats'],
            "rate_limited": security.get('rate_limited', False),
            "requires_https": security.get('requires_https', False),
            "requires_auth": security.get('requires_auth', False),
            "cors_enabled": security.get('cors_enabled', False),
            "security_score": "High" if security.get('requires_auth') and security.get('requires_https') else "Medium",
            "summary": summary,
            "message": f"Complete analysis: {len(endpoints)} endpoints found, {auth_info['primary']} auth detected"
        }
        
        # Save to history
        try:
            history_service.save_analysis(request.url or "uploaded", response_data)
        except Exception as e:
            # Log but don't fail if history save fails
            print(f"Warning: Could not save analysis to history: {e}")
        
        return response_data
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in full analysis: {str(e)}"
        )
