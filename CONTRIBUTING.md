# Contributing to Smart DevTool

Thank you for your interest in contributing! This guide will help you get started.

---

## 🎯 Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow
- Report issues constructively

---

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Smart-DevTool-for-API-Integration.git
   cd Smart-DevTool-for-API-Integration
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   - Backend: See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
   - Frontend: `cd frontend && npm install`

4. **Make your changes**
   - Write clean, documented code
   - Add tests where applicable
   - Follow existing code style

5. **Test locally**
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd frontend && npm run test
   ```

6. **Commit with clear messages**
   ```bash
   git commit -m "feat: Add feature description"
   ```

7. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

---

## 📝 Commit Message Guide

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (no logic change)
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Test addition/modification
- `chore:` Build, dependencies

### Examples

```bash
# Good
git commit -m "feat: Add endpoint extraction from URLs"

# Good
git commit -m "fix: Handle authentication errors gracefully

- Added retry logic for 401 errors
- Improved error message clarity
- Added logging for debugging"

# Avoid
git commit -m "fixed stuff"
git commit -m "update code"
```

---

## 🔄 Pull Request Process

### Before Creating PR

1. **Update from main**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run tests locally**
   ```bash
   cd backend && pytest
   cd frontend && npm run lint
   ```

3. **Check code style**
   ```bash
   # Backend
   pylint backend/
   
   # Frontend
   npm run lint
   ```

### PR Template

```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Related Issues
Closes #(issue number)

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No console errors
- [ ] Tests pass locally
```

---

## 🎨 Code Style Guide

### Python (Backend)

**Follow PEP 8** with these additions:

```python
# Type hints required
def extract_endpoints(
    documentation: str,
    max_results: int = 50
) -> List[Dict[str, Any]]:
    """
    Extract API endpoints from documentation.
    
    Args:
        documentation: Raw API documentation text
        max_results: Maximum endpoints to extract
    
    Returns:
        List of extracted endpoint dictionaries
    
    Raises:
        ValueError: If documentation is empty
    """
    if not documentation:
        raise ValueError("Documentation cannot be empty")
    
    # Implementation here
    pass
```

**Key Rules:**
- Use type hints for all functions
- Docstrings for public functions
- Maximum line length: 100 characters
- Snake_case for functions/variables
- UPPER_CASE for constants

### JavaScript/React (Frontend)

**Follow Airbnb style guide** with additions:

```javascript
// Props validation required
DocumentUpload.propTypes = {
  onAnalyze: PropTypes.func.isRequired,
  apiName: PropTypes.string,
  isLoading: PropTypes.bool,
};

DocumentUpload.defaultProps = {
  apiName: 'Unknown API',
  isLoading: false,
};

export default DocumentUpload;
```

**Key Rules:**
- Use functional components with hooks
- PropTypes for validation
- camelCase for variables/functions
- PascalCase for components
- 80 character line length preference

---

## 📚 Directory Structure Rules

### Backend Files
```
backend/
├── routes/          # API endpoints (one file per resource)
├── services/        # Business logic
├── agents/          # Multi-agent system
├── models/          # Pydantic schemas
├── utils/           # Utilities & helpers
└── tests/           # Tests (mirror structure)
```

### Frontend Files
```
frontend/src/
├── pages/           # Full page components
├── components/      # Reusable components
├── hooks/           # Custom React hooks
├── stores/          # Zustand stores
├── styles/          # Global styles
└── __tests__/       # Tests (mirror structure)
```

---

## 🧪 Testing Requirements

### Backend Tests

```python
# tests/test_api_analyzer.py
import pytest
from services.api_analyzer import extract_endpoints

def test_extract_endpoints_simple():
    """Test basic endpoint extraction"""
    doc = "GET /users/{id}"
    endpoints = extract_endpoints(doc)
    
    assert len(endpoints) == 1
    assert endpoints[0]['method'] == 'GET'
    assert endpoints[0]['path'] == '/users/{id}'

def test_extract_endpoints_empty():
    """Test handling of empty input"""
    with pytest.raises(ValueError):
        extract_endpoints("")
```

**Run tests:**
```bash
cd backend
pytest                    # All tests
pytest -v               # Verbose
pytest tests/test_*.py  # Specific file
```

### Frontend Tests

```javascript
// src/__tests__/DocumentUpload.test.jsx
import { render, screen } from '@testing-library/react';
import DocumentUpload from '../components/DocumentUpload';

describe('DocumentUpload', () => {
  it('renders upload button', () => {
    render(<DocumentUpload />);
    expect(screen.getByText(/upload/i)).toBeInTheDocument();
  });
});
```

**Run tests:**
```bash
cd frontend
npm run test         # Watch mode
npm run test -- --coverage  # With coverage
```

---

## 🐛 Bug Reports

### Good Bug Report
```
Title: Auth detection fails for OAuth 2.0 endpoints

Description:
When analyzing a GitHub API documentation with OAuth 2.0 flow,
the auth detector returns "bearer_token" instead of "oauth2".

Steps to reproduce:
1. Go to homepage
2. Paste https://docs.github.com/en/rest/overview/...
3. Click analyze
4. Check auth detection

Expected: Auth type = "oauth2"
Actual: Auth type = "bearer_token"

Environment: Windows 10, Chrome 120
```

---

## 🎯 Good First Issues

Look for issues tagged with:
- `good-first-issue` — Easy to start with
- `help-wanted` — Community help appreciated
- `documentation` — Doc improvements needed

---

## 🤔 Questions?

- **Issues:** [GitHub Issues](https://github.com/Sonuolikkara/Smart-DevTool-for-API-Integration/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Sonuolikkara/Smart-DevTool-for-API-Integration/discussions)
- **Email:** sonu@example.com

---

## 🎓 Learning Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [React Hooks Guide](https://react.dev/reference/react)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [LangChain Docs](https://python.langchain.com/)

---

## 📈 Development Workflow

### Feature Development

```
1. Create issue with `feature` label
2. Create branch from `main`
3. Develop & test locally
4. Create PR with issue reference
5. Code review by maintainers
6. Merge to main
7. Deploy to staging
8. Deploy to production
```

### Bug Fixes

```
1. Create issue with `bug` label
2. Create branch for fix
3. Write failing test first (TDD)
4. Fix the bug
5. Test passes
6. Create PR
7. Review & merge
```

### Documentation

```
1. Update relevant .md files
2. Run locally to verify formatting
3. Create PR with `docs` label
4. Quick review & merge
```

---

## 🚀 Next Steps After PR Merge

After your PR is merged:

1. ✅ Code reviewed by 2+ maintainers
2. ✅ All tests passing
3. ✅ Documentation updated
4. ✅ Deployed to staging
5. ✅ Verified in production

**Thank you for contributing!** 🎉

---

**Last Updated:** January 1, 2024 | v1.0
