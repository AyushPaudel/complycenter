from fastapi import FastAPI

from lifespan import lifespan_setup
from api.v1 import v1router
from core.logger import get_logger

# Initialize logger
logger = get_logger("main")


app = FastAPI(
    title="ComplyCentre API",
    description="API for managing cleaning operations across multiple business locations.",
    version="1.0.0",
    lifespan=lifespan_setup,
)


@app.get("/health", include_in_schema=False)
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "message": "ComplyCentre API is running"}


app.include_router(v1router)
