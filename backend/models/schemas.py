"""
Pydantic models and schemas for API requests/responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class EndpointParameter(BaseModel):
    """API endpoint parameter"""
    name: str
    type: str  # "string", "integer", "boolean", etc.
    required: bool = False
    description: Optional[str] = None
    location: str = "query"  # "query", "path", "body", "header"


class APIEndpoint(BaseModel):
    """Extracted API endpoint"""
    method: str  # GET, POST, PUT, DELETE, PATCH
    path: str
    description: Optional[str] = None
    parameters: List[EndpointParameter] = []
    request_body: Optional[Dict[str, Any]] = None
    response_format: Optional[Dict[str, Any]] = None
    rate_limit: Optional[str] = None
    authentication_required: bool = False


class AuthenticationMethod(BaseModel):
    """Detected authentication method"""
    type: str  # "bearer", "api_key", "basic", "oauth2", "custom"
    location: str  # "header", "query", "body"
    header_name: Optional[str] = None
    parameter_name: Optional[str] = None
    description: Optional[str] = None
    example: Optional[str] = None


class APIAnalysisResult(BaseModel):
    """Complete API analysis result"""
    api_name: str
    endpoints: List[APIEndpoint]
    authentication: Optional[AuthenticationMethod] = None
    base_url: Optional[str] = None
    version: Optional[str] = None
    rate_limits: Optional[Dict[str, str]] = None
    documentation_url: Optional[str] = None


class CodeGenerationRequest(BaseModel):
    """Request for code generation"""
    endpoints: List[APIEndpoint]
    auth_method: Optional[AuthenticationMethod] = None
    language: str = "python"  # python, javascript, typescript, go, java
    use_sdk: bool = False
    api_name: str
    include_tests: bool = False


class CodeGenerationResponse(BaseModel):
    """Response with generated code"""
    language: str
    code: str
    import_statements: List[str]
    setup_instructions: str
    example_usage: str
    execution_time_ms: float
