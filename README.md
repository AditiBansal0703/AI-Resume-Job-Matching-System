# AI-Powered Resume Parser — Hackathon Starter

**Version:** 1.0  
**Generated:** 2025-11-04

This starter repository contains a functional baseline for the AI-Powered Resume Parser Hackathon:
- FastAPI backend with endpoints for uploading resumes, checking status, retrieving parsed JSON, and matching to a job description.
- Simple parser pipeline supporting PDF (text-based), DOCX, TXT and image OCR (Tesseract).
- Minimal AI-enhancement hooks (OpenAI / local LLM optional).
- PostgreSQL-ready SQLAlchemy models.
- Docker & docker-compose for local deployment.
- Tests (pytest) with a small API smoke test.

## Quickstart (local, development)

1. Install dependencies (recommended inside venv):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Start a Postgres container or use Docker Compose:
```bash
docker-compose up --build
```

3. Run the API (if not using docker):
```bash
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open Swagger UI:
```
http://localhost:8000/docs
```

## Files of interest
- `src/app/main.py` — FastAPI app and endpoints
- `src/app/parsers.py` — Resume parsing logic (PDF, DOCX, TXT, images)
- `src/app/models.py` — SQLAlchemy models and DB utilities
- `docker/Dockerfile`, `docker-compose.yml`
- `docs/api-specification.yaml` — OpenAPI starter
- `tests/test_api.py` — pytest basic tests

## Notes
- Tesseract OCR and system libraries may be required for OCR on images/PDFs.
- OpenAI integration is optional; set `OPENAI_API_KEY` in `.env` to enable AI enhancements.
- This repository is a robust starting point — extend, experiment, and innovate!

Good luck — build something amazing! 🚀
