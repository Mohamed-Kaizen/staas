"""The app for staas."""
import logging
import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware

from staas.logger import InterceptHandler, log_format
from staas.settings import settings
from staas.super import supertokens

supertokens()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)
app.add_middleware(get_middleware())

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS + get_all_cors_headers(),
)

if __name__ == "__main__":
    uvicorn.run(
        "staas.main:app",
        host="0.0.0.0",  # noqa: S104
        port=settings.PORT,
        log_level="info",
        reload=settings.DEBUG,
    )

logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": logging.INFO,
            "format": log_format,
        }
    ]
)
logger.add("logs/file_{time:YYYY-MM-DD}.log", level="TRACE", rotation="1 day")
