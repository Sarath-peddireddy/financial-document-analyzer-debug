from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid
import json

from db import init_db, SessionLocal, User, Analysis
from tools import analyze_document

load_dotenv()
init_db()

app = FastAPI(title="Financial Document Analyzer")

cors_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
cors_list = [o.strip() for o in cors_env.split(",")] if cors_env else ["*"]
app.add_middleware(CORSMiddleware, allow_origins=cors_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class AnalyzeResponse(BaseModel):
    status: str
    query: str
    analysis: dict
    file_processed: str
    analysis_id: int

class AnalysisRecord(BaseModel):
    id: int
    filename: str
    query: str
    result: dict
    created_at: str

@app.get("/")
async def health():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...), query: str = Form(default=""), username: str = Form(default="anonymous")):
    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", f"upload_{file_id}.pdf")
    db = SessionLocal()
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        q = query.strip() or "Analyze this financial document for investment insights"
        result = analyze_document(file_path, q)
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        analysis = Analysis(user_id=user.id, filename=file.filename, query=q, result_json=json.dumps(result))
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return AnalyzeResponse(status="success", query=q, analysis=result, file_processed=file.filename, analysis_id=analysis.id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    finally:
        db.close()
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

@app.get("/analysis/{analysis_id}", response_model=AnalysisRecord)
def get_analysis(analysis_id: int):
    db = SessionLocal()
    try:
        rec = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not rec:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return AnalysisRecord(id=rec.id, filename=rec.filename, query=rec.query, result=json.loads(rec.result_json), created_at=rec.created_at.isoformat())
    finally:
        db.close()