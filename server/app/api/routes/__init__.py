from fastapi import APIRouter
from server.api.routes import intercepts

router = APIRouter()

router.include_router(intercepts.router)

