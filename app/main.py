from app.core.config import settings
from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.logging_setup import setup_root_logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# setup root logger
setup_root_logger()

# Get logger for module
LOGGER = logging.getLogger(__name__)


LOGGER.info("---Starting App---")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health():
    return {"message": "ok!"}
