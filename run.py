import uvicorn
import sys
import os

def start():
    """Starts the AeroMind backend server."""
    print("🚀 Starting AeroMind Backend...")
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )

if __name__ == "__main__":
    start()
