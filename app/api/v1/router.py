from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.medications import router as medications_router
from app.api.v1.endpoints.doses import router as doses_router

api_v1_router = APIRouter()

api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(medications_router, prefix="/medications", tags=["medications"])
api_v1_router.include_router(doses_router, prefix="/doses", tags=["doses"])
