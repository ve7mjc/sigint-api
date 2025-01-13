from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.database import Base, engine

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)  # , prefix="/api"