# Financial Document Analyzer

## Overview

A robust AI-powered system for analyzing financial documents (PDFs) and generating investment insights, recommendations, and risk assessments.  
Now includes a lightweight SQLite database for storing user info and analysis results.

---

## 🐞 Bugs Fixed

- **LLM Initialization:** Fixed undefined LLM object; now properly initialized in `agents.py`.
- **Agent Parameters:** Corrected `tool` to `tools`, set `memory` to `False` for stateless operation.
- **PDF Loader:** Imported and used the correct PDF loader in `tools.py`.
- **Prompt Templates:** Shortened and structured all LLM prompts using JSON schema and bullet points for reliability.
- **File Handling:** Improved file upload and cleanup logic in `main.py`.
- **Consistency:** Unified agent/task interfaces and improved error handling.
- **Database Integration:** Added SQLite support for storing analysis results and user info.

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

## 👩‍💻 Developer Usage Guide

- **Agents:**  
  Defined in [`agents.py`](financial-document-analyzer-debug/agents.py). Customize agent roles, goals, and tools as needed.

- **Tasks:**  
  Defined in [`task.py`](financial-document-analyzer-debug/task.py). Use structured prompt templates for reliable LLM output.

- **Tools:**  
  Extend [`tools.py`](financial-document-analyzer-debug/tools.py) to add new document parsers or analysis utilities.

- **Database:**  
  - Models and setup in [`db.py`](financial-document-analyzer-debug/db.py).
  - Uses SQLite (`financial_analyzer.db`) for storing users and analysis results.
  - ORM via SQLAlchemy for easy extension.

- **Adding Features:**  
  - To add a queue worker, integrate Celery or RQ and refactor `/analyze` to enqueue jobs.
  - For more advanced user management, extend the `User` model and authentication logic.

---

## 📦 Extending the System

- **Queue Worker:**  
  Integrate Celery/RQ for concurrent request handling (not included by default).

- **Database Integration:**  
  Store user info and analysis results for future reference and analytics.  
  Easily switch to PostgreSQL or MySQL by updating the `DATABASE_URL` in `db.py`.

---

## License

MIT License

---