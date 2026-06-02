# Architecture Documentation

## System Overview

Smart DevTool for API Integration is a full-stack application that uses local AI (Ollama) to analyze API documentation and generate production-ready wrapper code.

### High-Level Flow

```
User Input (API Docs)
        ↓
    Frontend
  (React UI)
        ↓
    FastAPI Backend
    (Routes & Logic)
        ↓
   Multi-Agent System
   ├─ Scraper Agent
   ├─ Analyzer Agent
   └─ Generator Agent
        ↓
   Ollama (Local LLM)
   └─ qwen2.5-coder
        ↓
   Output (Generated Code)
        ↓
    Frontend Display
  (Syntax Highlighting)
```

---

## Frontend Architecture (React)

### Pages

1. **Home.jsx** (`/`)
   - Landing page with problem/solution overview
   - Upload component for API documentation
   - Example APIs quick-start
   - Feature highlights

2. **Workspace.jsx** (`/workspace`)
   - Main analysis and code generation workspace
   - Split view: Input (left) + Output (right)
   - Real-time execution tracing
   - Language selector
   - Copy/download buttons

3. **History.jsx** (`/history`)
   - Saved integrations list
   - Re-analyze with different settings
   - Export/share options
   - Search and filter

### Components

- **DocumentUpload.jsx** — Upload form for API documentation
- **APIAnalyzer.jsx** — Display extracted endpoints
- **CodeGenerator.jsx** — Generate wrapper code UI
- **CodeViewer.jsx** — Syntax-highlighted code display
- **ExecutionViewer.jsx** — Step-by-step progress animation
- **EndpointCard.jsx** — Individual endpoint visualization
- **AuthenticationPanel.jsx** — Auth method display
- **LoadingAnimation.jsx** — Smooth loading states

### Hooks

- **useAPIIntegration.js** — Manages API analysis state
- **useCodeGeneration.js** — Manages code generation state

### State Management

Using **Zustand** for lightweight state:
```javascript
// Global store for:
// - Current API documentation
// - Extracted endpoints
// - Selected language
// - Generated code
// - History/saved items
```

### Styling

- **TailwindCSS** — Utility-first CSS framework
- **Framer Motion** — Smooth animations and transitions
- **Prism.js** — Code syntax highlighting
- **Dark theme** — Professional dark mode by default

---

## Backend Architecture (FastAPI)

### Entry Point: main.py

```python
FastAPI Application
├─ CORS Middleware (frontend access)
├─ Routes:
│  ├─ /api/documents (upload & parse)
│  ├─ /api/analysis (endpoint extraction)
│  └─ /api/generation (code generation)
└─ Health endpoints
```

### Routes

#### 1. **routes/documents.py**
```
POST /api/documents/upload
  - Accept: URL, raw text, or file upload
  - Returns: Cleaned documentation text
  - Uses: BeautifulSoup, Playwright, aiohttp

GET /api/documents/{doc_id}
  - Retrieve stored documentation
```

#### 2. **routes/analysis.py**
```
POST /api/analysis/endpoints
  - Input: documentation text
  - Output: Extracted endpoints list
  - Example: [{"method": "GET", "path": "/users/{id}", ...}]

POST /api/analysis/auth
  - Input: documentation text
  - Output: Auth method detected
  - Example: {"type": "bearer", "location": "header", ...}

POST /api/analysis/parameters
  - Input: endpoint documentation
  - Output: Required parameters
```

#### 3. **routes/generation.py**
```
POST /api/generation/wrapper
  - Input: endpoints, auth, language
  - Output: Generated wrapper code
  - Uses: Ollama + qwen2.5-coder model

POST /api/generation/tests
  - Input: wrapper code
  - Output: Generated test cases

POST /api/generation/documentation
  - Input: wrapper code
  - Output: Generated API documentation
```

### Services

#### **services/ollama_service.py**
```python
class OllamaService:
    async def generate_text(prompt: str, model: str) -> str
    async def generate_code(prompt: str, temperature: float) -> str
    async def generate_embeddings(text: str) -> List[float]
    async def health_check() -> bool
```

#### **services/rag_pipeline.py**
```python
class RAGPipeline:
    async def setup(documentation: str)
    async def query(question: str) -> str
    async def semantic_search(query: str, top_k: int) -> List[str]
```

Uses:
- **LangChain** — Framework for LLM orchestration
- **ChromaDB** — Vector storage
- **nomic-embed-text** — Local embeddings model

#### **services/doc_processor.py**
```python
class DocumentProcessor:
    async def fetch_from_url(url: str) -> str
    def parse_html_docs(html: str) -> str
    def parse_markdown_docs(md: str) -> str
    def chunk_documentation(text: str, chunk_size: int) -> List[str]
```

#### **services/api_analyzer.py**
```python
class APIAnalyzer:
    def extract_endpoints(doc_text: str) -> List[Dict]
    def extract_parameters(endpoint_doc: str) -> List[Dict]
    def identify_response_format(doc_text: str) -> Dict
    def detect_rate_limits(doc_text: str) -> Dict
```

Uses regex patterns and NLP for intelligent extraction.

#### **services/auth_detector.py**
```python
class AuthDetector:
    def detect_auth_method(doc_text: str) -> Dict
    def identify_auth_location(doc_text: str) -> str
    def generate_auth_example(auth_info: Dict) -> str
```

Detects:
- Bearer Token (JWT, OAuth)
- API Key (header, query, body)
- Basic Auth
- OAuth 2.0
- Custom headers

#### **services/code_generator.py**
```python
class CodeGenerator:
    async def generate_wrapper_code(
        api_name: str,
        endpoints: List[Dict],
        auth_method: Dict,
        language: str,
        doc_context: str
    ) -> str
```

Generates:
- Class structure
- Method implementations
- Error handling & retry logic
- Type hints
- Docstrings
- Example usage

#### **services/sdk_suggester.py**
```python
class SDKSuggester:
    def check_sdk_availability(api_name: str, language: str) -> bool
    def suggest_sdk_or_rest(api_info: Dict) -> Dict
    def generate_comparison(api_info: Dict) -> str
```

#### **services/vector_db.py**
```python
class VectorDB:
    async def store_embeddings(chunks: List[str], embeddings: List)
    async def query(query_text: str, top_k: int) -> List[str]
    async def delete_collection(collection_id: str)
```

### Agents

Multi-agent system for parallel processing:

#### **agents/scraper_agent.py**
- Fetch documentation from URL
- Clean and normalize text
- Handle multiple document formats

#### **agents/analyzer_agent.py**
- Extract endpoints using patterns
- Detect authentication methods
- Identify parameters and response formats
- Generate semantic summaries

#### **agents/generator_agent.py**
- Generate code using Ollama
- Apply language-specific templates
- Add error handling and retry logic
- Generate documentation

#### **agents/orchestrator.py**
```python
class Orchestrator:
    async def analyze_api(input_source: str) -> Dict
    async def generate_code(analysis_result: Dict, language: str) -> str
    async def execute_workflow(user_request: Dict) -> Dict
```

Coordinates all agents and manages task flow.

### Models (Pydantic Schemas)

#### **models/schemas.py**
```python
class Endpoint(BaseModel):
    method: str  # GET, POST, etc.
    path: str
    description: str
    parameters: List[Parameter]
    response: ResponseSchema

class Parameter(BaseModel):
    name: str
    type: str
    required: bool
    description: str

class APIAnalysisResult(BaseModel):
    endpoints: List[Endpoint]
    auth_method: Dict
    base_url: str
    rate_limits: Dict

class GeneratedCode(BaseModel):
    language: str
    code: str
    dependencies: List[str]
    installation_command: str
    example_usage: str
```

### Configuration

#### **config.py**
```python
class Settings:
    # API Configuration
    API_TITLE: str
    API_VERSION: str
    
    # CORS Configuration
    CORS_ORIGINS: List[str]
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str
    OLLAMA_PRIMARY_MODEL: str
    OLLAMA_FALLBACK_MODEL: str
    OLLAMA_EMBEDDING_MODEL: str
    
    # Database Configuration
    CHROMADB_PATH: str
    
    # Processing Configuration
    MAX_CHUNK_SIZE: int
    EMBEDDING_BATCH_SIZE: int
    
    # Timeout Configuration
    REQUEST_TIMEOUT: int
    OLLAMA_TIMEOUT: int
```

### Data Structures

#### **data/sdk_templates/**
- `python_wrapper.template`
- `javascript_wrapper.template`
- `typescript_wrapper.template`
- `go_wrapper.template`
- `java_wrapper.template`

Templates include:
- Basic class structure
- Error handling patterns
- Authentication setup
- Request/response handling
- Docstring placeholders

### Utilities

#### **utils/prompts.py**
```python
# LLM Prompts for:
# - Endpoint extraction
# - Auth detection
# - Code generation
# - Test generation
# - Documentation generation
```

#### **utils/chunking.py**
```python
def chunk_text(text: str, chunk_size: int) -> List[str]
def chunk_by_sections(text: str) -> List[str]
def chunk_by_semantics(text: str) -> List[str]
```

#### **utils/formatting.py**
```python
def format_code(code: str, language: str) -> str
def format_endpoint_display(endpoint: Dict) -> str
def format_error_message(error: Exception) -> str
```

---

## Data Flow

### Analysis Flow

```
User Input (API Docs URL/Text)
        ↓
    DocumentProcessor
    (Fetch & Parse)
        ↓
    RAGPipeline
    (Create Embeddings & Store)
        ↓
    APIAnalyzer
    (Extract Endpoints & Auth)
        ↓
    Frontend Display
    (Endpoint Cards, Auth Panel)
```

### Code Generation Flow

```
Selected Configuration
(endpoints, auth, language)
        ↓
    CodeGenerator
    (Create Prompt with Context)
        ↓
    OllamaService
    (Call qwen2.5-coder)
        ↓
    Post-Processing
    (Format, Validate, Add Examples)
        ↓
    Frontend Display
    (Syntax-Highlighted Code)
```

---

## Database Schema

### ChromaDB Collections

#### **api_documentation**
```
{
  id: "stripe_v1",
  document: "Full Stripe API docs text",
  metadata: {
    api_name: "Stripe",
    created_at: "2024-01-01",
    chunk_index: 0
  }
}
```

#### **generated_code**
```
{
  id: "stripe_python_jwt",
  document: "Generated Python wrapper code",
  metadata: {
    api_name: "Stripe",
    language: "python",
    auth_type: "jwt",
    created_at: "2024-01-01"
  }
}
```

---

## Deployment Architecture

### Development
```
Frontend (npm run dev)
  ↓
Vite (http://localhost:5173)

Backend (uvicorn main:app --reload)
  ↓
FastAPI (http://localhost:8000)

Ollama (ollama serve)
  ↓
LLM Service (http://localhost:11434)
```

### Production
```
Frontend
  ↓
Nginx / Vercel / Netlify
  ↓
Static assets (React build)

Backend
  ↓
Gunicorn / Docker Container
  ↓
FastAPI on Cloud (AWS/Azure/GCP)

Ollama
  ↓
GPU Instance or Docker Container
  ↓
LLM Service
```

---

## Security Considerations

1. **CORS** — Only allow frontend domain
2. **Input Validation** — Pydantic models validate all inputs
3. **Rate Limiting** — Prevent abuse (todo: Day 6)
4. **Local Processing** — No external API calls (privacy)
5. **Error Handling** — No sensitive info in error messages
6. **Environment Variables** — Secure config management

---

## Performance Optimization

1. **Async Processing** — All I/O operations are async
2. **Caching** — Embeddings cached in ChromaDB
3. **Chunking** — Large documents processed in chunks
4. **Model Optimization** — qwen2.5-coder is lightweight
5. **Frontend Optimization** — Code splitting with Vite

---

## Monitoring & Logging

### Backend Logging
```python
logger.info("Event description")
logger.error("Error with context", exc_info=True)
logger.debug("Detailed execution trace")
```

### Frontend Error Tracking
- React Error Boundary (todo: Day 6)
- Console error logging
- Graceful error displays with user guidance

---

## Future Architecture Improvements

- [ ] WebSocket for real-time updates
- [ ] Distributed task queue (Celery)
- [ ] GraphQL API layer
- [ ] Multi-tenant support
- [ ] Advanced caching strategies
- [ ] Horizontal scaling

---

**Last Updated:** January 1, 2024 | v1.0
