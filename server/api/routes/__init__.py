from fastapi import APIRouter
from app.api.routes import intercepts

router = APIRouter()

router.include_router(intercepts.router)

