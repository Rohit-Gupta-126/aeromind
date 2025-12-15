from fastapi import FastAPI
from app.api.routes import router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("aeromind.log")
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="AeroMind")

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "AeroMind system online",
        "status": "OK"
    }
