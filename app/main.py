from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.lifespan import lifespan_setup
from app.api.v1 import v1router
from app.core.logger import get_logger

# Initialize logger
logger = get_logger("main")


app = FastAPI(
    title="ComplyCentre API",
    description="API for managing cleaning operations across multiple business locations.",
    version="1.0.0",
    lifespan=lifespan_setup,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods; restrict in production
    allow_headers=["*"],  # Allow all headers; restrict in production
)

@app.get("/health", include_in_schema=False)
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "message": "ComplyCentre API is running"}


app.include_router(v1router)
