# Financial Document Analyzer

## Overview

A robust AI-powered system for analyzing financial documents (PDFs) and generating investment insights, recommendations, and risk assessments.  
Now includes a lightweight SQLite database for storing user info and analysis results.

---

## Stack

- FastAPI API server
- SQLite via SQLAlchemy ORM
- Simple PDF parsing and heuristic analysis utilities
- Frontend: HTML/CSS/Vanilla JS
- OpenAI integration for analysis (fallback to heuristics if not configured)

---

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd financial-document-analyzer-debug
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Environment:**
   - Copy `.env.example` to `.env` and set values:
     ```
     OPENAI_API_KEY=sk-...
     OPENAI_MODEL=gpt-4o-mini
     CORS_ALLOW_ORIGINS=*
     DATABASE_URL=sqlite:///./financial_analyzer.db
     ```

3. **Add a sample PDF:**
   - Download a financial report (e.g., Tesla Q2 2025) and save as `data/sample.pdf`.

---

## 🏃 How to Run

1. **Start the API server:**
   ```sh
   uvicorn main:app --reload
   ```

2. **API Endpoints:**

   - **Health Check:**  
     `GET /`  
     Response:  
     ```json
     {"message": "Financial Document Analyzer API is running"}
     ```

   - **Analyze Document:**  
     `POST /analyze`  
     Form Data:  
     - `file`: PDF file to analyze  
     - `query`: (optional) Analysis query  
     - `username`: (optional) Username for tracking  
     Response:  
     ```json
     {
       "status": "success",
       "query": "Your query",
       "analysis": {
         "summary": "...",
         "insights": [...],
         "recommendations": [...],
         "risks": [...],
         "references": [...]
       },
       "file_processed": "filename.pdf",
       "analysis_id": 1
     }
     ```

   - **Retrieve Past Analysis:**  
     `GET /analysis/{analysis_id}`  
     Response:  
     ```json
     {
       "id": 1,
       "filename": "filename.pdf",
       "query": "Your query",
       "result": "...",
       "created_at": "2025-08-26T12:34:56"
     }
     ```

---

## 👩‍💻 Developer Notes

- API in `main.py`
- ORM and models in `db.py`
- PDF parsing and analysis in `tools.py`
- Frontend in `frontend/`

- **Adding Features:**  
  - To add a queue worker, integrate Celery or RQ and refactor `/analyze` to enqueue jobs.
  - For more advanced user management, extend the `User` model and authentication logic.

---

## Frontend

Open `frontend/index.html` in a browser. Set the API base URL at the top of `frontend/app.js` (default: `http://localhost:8000`).

If serving frontend from another origin, ensure `CORS_ALLOW_ORIGINS` includes that origin.

---

## License

MIT License

---