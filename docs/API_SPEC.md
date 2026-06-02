# API Specification

Complete REST API reference for Smart DevTool backend.

---

## Base URL

**Development:** `http://localhost:8000`

**Production:** `https://api.smartdevtool.com` (future)

---

## Health Endpoints

### GET /

Get API information and available endpoints.

**Response:**
```json
{
  "service": "Smart DevTool for API Integration",
  "version": "1.0.0",
  "status": "active",
  "endpoints": {
    "health": "/health",
    "docs": "/docs",
    "redoc": "/redoc"
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Smart DevTool API",
  "version": "1.0.0"
}
```

---

## Documents API

### POST /api/documents/upload

Upload or provide API documentation.

**Request:**
```json
{
  "source_type": "url|text|file",
  "content": "https://api.example.com/docs or raw text",
  "api_name": "Example API",
  "format": "html|markdown|json"
}
```

**Response:**
```json
{
  "document_id": "doc_12345",
  "status": "processed",
  "text_length": 45000,
  "preview": "API Documentation for Example...",
  "extracted_sections": 15,
  "processing_time_ms": 1234
}
```

**Status Codes:**
- `200` — Success
- `400` — Invalid input
- `413` — File too large
- `500` — Processing error

---

### GET /api/documents/{document_id}

Retrieve stored documentation.

**Response:**
```json
{
  "document_id": "doc_12345",
  "api_name": "Example API",
  "content": "Full documentation text...",
  "created_at": "2024-01-01T12:00:00Z",
  "source": "https://api.example.com/docs"
}
```

---

## Analysis API

### POST /api/analysis/endpoints

Extract API endpoints from documentation.

**Request:**
```json
{
  "document_id": "doc_12345",
  "or_text": "Raw documentation text"
}
```

**Response:**
```json
{
  "status": "success",
  "endpoints_found": 24,
  "endpoints": [
    {
      "id": "endpoint_1",
      "method": "GET",
      "path": "/api/users/{id}",
      "description": "Get user by ID",
      "parameters": [
        {
          "name": "id",
          "type": "string",
          "required": true,
          "description": "User ID"
        }
      ],
      "response": {
        "status": 200,
        "content_type": "application/json",
        "schema": "User object"
      }
    }
  ],
  "processing_time_ms": 2150
}
```

---

### POST /api/analysis/auth

Detect authentication method from documentation.

**Request:**
```json
{
  "document_id": "doc_12345"
}
```

**Response:**
```json
{
  "status": "detected",
  "auth_methods": [
    {
      "type": "bearer_token",
      "location": "header",
      "header_name": "Authorization",
      "format": "Bearer {token}",
      "description": "JWT Bearer token authentication",
      "examples": [
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
      ],
      "how_to_get": "https://docs.example.com/auth"
    }
  ],
  "confidence": 0.98
}
```

---

### POST /api/analysis/parameters

Extract and analyze parameters from endpoints.

**Request:**
```json
{
  "endpoint_path": "/api/payments",
  "method": "POST",
  "document_id": "doc_12345"
}
```

**Response:**
```json
{
  "status": "success",
  "endpoint": "/api/payments",
  "method": "POST",
  "parameters": {
    "path": [],
    "query": [],
    "header": [
      {
        "name": "Authorization",
        "type": "string",
        "required": true,
        "description": "Bearer token"
      }
    ],
    "body": [
      {
        "name": "amount",
        "type": "integer",
        "required": true,
        "description": "Amount in cents",
        "example": 10000
      },
      {
        "name": "currency",
        "type": "string",
        "required": false,
        "description": "ISO 4217 currency code",
        "example": "usd"
      }
    ]
  }
}
```

---

## Generation API

### POST /api/generation/wrapper

Generate wrapper code for the API.

**Request:**
```json
{
  "document_id": "doc_12345",
  "endpoints": [
    {
      "method": "GET",
      "path": "/api/users/{id}"
    }
  ],
  "auth_method": {
    "type": "bearer_token",
    "header_name": "Authorization"
  },
  "language": "python",
  "use_sdk": false,
  "include_tests": true
}
```

**Response:**
```json
{
  "status": "success",
  "code": "class APIClient:\n    def __init__(self, api_key: str):\n        ...",
  "language": "python",
  "lines_of_code": 250,
  "dependencies": [
    "requests>=2.28.0",
    "pydantic>=1.10.0"
  ],
  "installation_command": "pip install requests pydantic",
  "example_usage": "client = APIClient(api_key)\nuser = await client.get_user(id='123')",
  "generation_time_ms": 1850
}
```

**Supported Languages:**
- `python`
- `javascript`
- `typescript`
- `go`
- `java`
- `ruby` (planned)
- `php` (planned)

---

### POST /api/generation/tests

Generate test cases for the wrapper code.

**Request:**
```json
{
  "wrapper_code": "class APIClient: ...",
  "language": "python",
  "framework": "pytest"
}
```

**Response:**
```json
{
  "status": "success",
  "test_code": "import pytest\nfrom api_client import APIClient\n\n@pytest.mark.asyncio\nasync def test_get_user(): ...",
  "test_framework": "pytest",
  "test_count": 8,
  "coverage_percentage": 85
}
```

---

### POST /api/generation/documentation

Generate comprehensive documentation for the wrapper.

**Request:**
```json
{
  "wrapper_code": "class APIClient: ...",
  "api_name": "Example API",
  "language": "python"
}
```

**Response:**
```json
{
  "status": "success",
  "documentation": "# Example API Client\n\n## Installation\n...\n\n## Usage\n...",
  "format": "markdown",
  "sections": [
    "Installation",
    "Configuration",
    "Authentication",
    "Usage Examples",
    "Error Handling",
    "API Reference"
  ]
}
```

---

## SDK Suggestion API

### POST /api/suggestions/sdk

Suggest SDK vs REST approach.

**Request:**
```json
{
  "api_name": "Stripe",
  "language": "python"
}
```

**Response:**
```json
{
  "status": "success",
  "api_name": "Stripe",
  "language": "python",
  "recommendations": [
    {
      "option": "sdk",
      "sdk_name": "stripe",
      "package_manager": "pip",
      "install_command": "pip install stripe",
      "version": "5.15.0",
      "pros": [
        "Official SDK by Stripe",
        "Full type hints",
        "Built-in retry logic",
        "Excellent documentation"
      ],
      "cons": [
        "External dependency",
        "Larger package size"
      ],
      "score": 9.5
    },
    {
      "option": "rest",
      "pros": [
        "Zero external dependencies",
        "Lightweight",
        "Full control"
      ],
      "cons": [
        "Manual error handling",
        "More boilerplate code"
      ],
      "score": 7.0
    }
  ],
  "recommended": "sdk",
  "reason": "Official SDK offers best practices and full type safety"
}
```

---

## Error Responses

All error responses follow this format:

**400 Bad Request:**
```json
{
  "status": "error",
  "error_code": "INVALID_INPUT",
  "message": "API documentation URL is invalid",
  "details": {
    "field": "url",
    "issue": "Invalid URL format"
  }
}
```

**404 Not Found:**
```json
{
  "status": "error",
  "error_code": "NOT_FOUND",
  "message": "Document not found",
  "document_id": "doc_12345"
}
```

**429 Too Many Requests:**
```json
{
  "status": "error",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests",
  "retry_after_seconds": 60
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "error_code": "INTERNAL_ERROR",
  "message": "An internal error occurred",
  "request_id": "req_abc123"
}
```

---

## Rate Limiting

- **Free Tier:** 100 requests/hour
- **Pro Tier:** 1,000 requests/hour (future)

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Authentication

**Future:** API key authentication (Day 5-6)

Currently all endpoints are public for development.

---

## CORS

**Allowed Origins:**
- `http://localhost:5173` (development frontend)
- `http://localhost:3000` (alternative)
- `http://127.0.0.1:5173`
- `https://smartdevtool.com` (production, future)

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers:** Content-Type, Authorization

---

## Webhooks

**Planned for Phase 2**

- `analysis.completed` — When endpoint extraction completes
- `generation.completed` — When code generation finishes
- `error.occurred` — On processing errors

---

## Pagination

List endpoints support pagination:

```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 150,
    "total_pages": 8
  }
}
```

---

## Versioning

Current API version: **v1**

Future versions will be supported at `/api/v2/...`

Backwards compatibility maintained for 2+ versions.

---

**Last Updated:** January 1, 2024 | API v1.0
