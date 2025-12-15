from fastapi import APIRouter, UploadFile, File, HTTPException
from app.graph.workflow import run_workflow
from app.models.schemas import QuestionRequest, FinalResponse
from app.core.vectordb import build_vector_db
import os
import shutil

router = APIRouter()

@router.post("/ask", response_model=FinalResponse)
def ask_question(payload: QuestionRequest):
    question = payload.question
    result = run_workflow(question)
    return result

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Define the path
    upload_dir = "data/documents"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    try:
        # 2. Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 3. Trigger Ingestion
        # This re-runs the logic found in scripts/ingest.py
        # Note: For large datasets, this might be slow as it re-indexes everything.
        build_vector_db()
        
        return {
            "filename": file.filename, 
            "status": "success", 
            "message": "File uploaded and knowledge base updated."
        }
    except Exception as e:
        # Clean up if something fails (optional but good practice)
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
