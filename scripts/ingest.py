import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.vectordb import build_vector_db

if __name__ == "__main__":
    build_vector_db()
    print("Document ingestion complete.")
