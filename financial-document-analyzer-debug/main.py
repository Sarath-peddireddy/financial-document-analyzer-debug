from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from db import init_db, SessionLocal, AnalysisResult
init_db()
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the CrewAI pipeline for document analysis."""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    username: str = Form(default="anonymous")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    db = SessionLocal()
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        if not query:
            query = "Analyze this financial document for investment insights"
        response = run_crew(query=query.strip(), file_path=file_path)
        # Save to DB
        analysis = AnalysisResult(
            user_id=0,  
            filename=file.filename,
            query=query,
            result=str(response)
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename,
            "analysis_id": analysis.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    finally:
        db.close()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
@app.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: int):
    db = SessionLocal()
    try:
        analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return {
            "id": analysis.id,
            "filename": analysis.filename,
            "query": analysis.query,
            "result": analysis.result,
            "created_at": analysis.created_at
        }
    finally:
        db.close()