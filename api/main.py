from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from api.routes import router
from common.logger import logger

app = FastAPI(
    title="High-Scale Production ML Engine",
    version="1.0.0",
    docs_url="/docs"
)

Instrumentator().instrument(app).expose(app)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing system dependencies and connections...")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "online"}