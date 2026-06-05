# Contributing to Smart DevTool

Thanks for helping improve Smart DevTool, the API documentation analysis and SDK generation app.

## Code of Conduct

Be respectful, keep feedback constructive, and focus on the code and behavior rather than the person.

## Project Setup

This repository has two main parts:
- Backend: FastAPI in `backend/`
- Frontend: React + Vite in `frontend/`

Recommended local setup:

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

If you prefer Docker, `docker-compose.yml` starts the full stack locally.

## Running the App

```bash
# Backend
cd backend
python main.py

# Frontend
cd frontend
npm run dev
```

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## What to Change

Please keep changes focused and small:
- one feature or fix per commit when possible
- add tests for behavior changes
- update docs if behavior or setup changes
- avoid committing build output, screenshots, or temporary files

## Commit Messages

Use clear, descriptive commit messages in this format:

```bash
git commit -m "fix: handle fetch timeout for documentation URLs"
git commit -m "feat: add results page for endpoint analysis"
git commit -m "docs: update setup instructions"
```

Good commit messages explain what changed and why. Avoid messages like `update` or `fix stuff`.

## Branching and Pull Requests

1. Create a branch from `main`.
2. Make a small, logical set of changes.
3. Test locally before opening a PR.
4. Include a short summary of what you changed and how you tested it.

Suggested PR checklist:
- [ ] Code runs locally
- [ ] Tests pass
- [ ] Documentation updated if needed
- [ ] No unnecessary files added

## Testing

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run test
```

If you change UI or API behavior, verify the main flow manually:
- fetch documentation from a valid URL
- inspect the extracted endpoints
- open the results page
- generate code from analysis results

## Code Style

Backend Python:
- use type hints where practical
- keep functions small and readable
- prefer explicit error handling
- follow existing FastAPI and Pydantic patterns

Frontend React:
- use functional components and hooks
- keep component state local unless shared state is needed
- follow the existing Tailwind and Framer Motion style used in the app

## Repository Rules

Please do not commit:
- screenshots or image dumps unless they are needed for documentation
- build artifacts such as `dist/`, `node_modules/`, or cache folders
- temporary context files or personal notes

## Reporting Issues

When reporting a bug, include:
- the URL or file you used
- the exact steps to reproduce
- what you expected
- what actually happened
- any console or backend error output

## Questions

Use GitHub Issues for bugs or feature requests.

**Last Updated:** June 2026
