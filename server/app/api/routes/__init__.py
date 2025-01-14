from fastapi import APIRouter
from app.api.routes import intercepts, nodes

router = APIRouter()

router.include_router(intercepts.router)
router.include_router(nodes.router)
