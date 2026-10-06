from fastapi import FastAPI

from app.core.config import settings
from app.routers import doses, health, medications, webhooks

app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.1.0',
)

app.include_router(health.router, tags=['health'])
app.include_router(
    medications.router, prefix='/medications', tags=['medications']
)
app.include_router(doses.router, prefix='/doses', tags=['doses'])
app.include_router(webhooks.router, prefix='/webhooks', tags=['webhooks'])
