from fastapi import APIRouter, UploadFile, File, HTTPException
from app.graph.workflow import run_workflow
from app.models.schemas import QuestionRequest, FinalResponse
from app.core.vectordb import build_vector_db
import os
import shutil

router = APIRouter()

# In-memory analytics store (USP Feature)
query_analytics = {
    "total_queries": 0,
    "queries_by_route": {"engineering": 0, "safety": 0, "unsupported": 0},
    "avg_response_time_ms": 0,
    "recent_queries": []
}

@router.post("/ask", response_model=FinalResponse)
def ask_question(payload: QuestionRequest):
    question = payload.question
    expert_mode = payload.expert_mode
    result = run_workflow(question, expert_mode)
    
    # Update analytics (USP Feature)
    query_analytics["total_queries"] += 1
    route = result.get("route_selected", "unsupported")
    if route in query_analytics["queries_by_route"]:
        query_analytics["queries_by_route"][route] += 1
    
    # Update average response time
    current_time = result.get("processing_time_ms", 0)
    total = query_analytics["total_queries"]
    prev_avg = query_analytics["avg_response_time_ms"]
    query_analytics["avg_response_time_ms"] = ((prev_avg * (total - 1)) + current_time) / total
    
    # Store recent query (keep last 10)
    query_analytics["recent_queries"].append({
        "question": question[:100],
        "route": route,
        "time_ms": current_time
    })
    query_analytics["recent_queries"] = query_analytics["recent_queries"][-10:]
    
    return result

@router.get("/analytics")
def get_analytics():
    """
    USP Feature: Query Analytics Dashboard
    Returns insights about query patterns and system performance.
    """
    return {
        "total_queries": query_analytics["total_queries"],
        "queries_by_route": query_analytics["queries_by_route"],
        "avg_response_time_ms": round(query_analytics["avg_response_time_ms"], 2),
        "recent_queries": query_analytics["recent_queries"],
        "status": "healthy"
    }

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
