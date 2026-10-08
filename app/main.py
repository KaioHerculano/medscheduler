from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.routers import doses, health, medications, webhooks
from app.workers.scheduler import create_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    scheduler = create_scheduler()
    if settings.ENVIRONMENT != 'test':
        scheduler.start()
    try:
        yield
    finally:
        if scheduler.running:
            scheduler.shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.1.0',
    lifespan=lifespan,
)

app.include_router(health.router, tags=['health'])
app.include_router(
    medications.router, prefix='/medications', tags=['medications']
)
app.include_router(doses.router, prefix='/doses', tags=['doses'])
app.include_router(webhooks.router, prefix='/webhooks', tags=['webhooks'])
