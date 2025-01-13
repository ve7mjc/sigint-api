from server.services.minio_service import upload_to_minio
from app.core.config import settings

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from sqlalchemy.orm import Session
from app.schemas.intercept import InterceptCreate, InterceptResponse, InterceptAudioCreate
from app.db.database import get_db
from app.db.models import Intercept, InterceptAudioFile
import json


router = APIRouter(
    prefix="/intercepts",
    tags=["intercepts"]
)

"""
we are using mult-part form data to send the json request along with a file upload
but this means the json data is encoded into a field
"""

@router.post("/", response_model=InterceptResponse)
async def create_intercept(
    intercept: str = Form(...),  # JSON string in the form
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:

        # parsing and validation of request
        intercept = json.loads(intercept)
        req = InterceptCreate(**intercept)

        # Read the file contents
        file_data = await file.read()

        mio = upload_to_minio(settings.MINIO_BUCKET_NAME, file.filename, file_data)

        new_intercept = Intercept(
            **intercept,
            audio_file = InterceptAudioFile(
                bucket_name=mio.bucket_name,
                object_name=mio.object_name,
                etag=mio.etag,
                size=len(file_data)
            )
        )

        # req.audio_file = InterceptAudioCreate(
        #     bucket_name=mio.bucket_name,
        #     object_name=mio.object_name,
        #     etag=mio.etag,
        #     size=len(file_data)
        # )

        # Use the validated schema object to create a database entry
        # new_intercept = InterceptCreate(
        #     node_id=req.node_id,
        #     time_start=req.time_start,
        #     duration=req.duration,
        #     audio_file = audio_file
        #     # json_data=intercept.json,
        #     # file_path=file_path,
        # )

        db.add(new_intercept)
        db.commit()
        db.refresh(new_intercept)

        return req
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"create_intercept failed: {e}")


    # new_intercept = Intercept(**intercept.dict())
    # db.add(new_intercept)
    # db.commit()
    # db.refresh(new_intercept)
    # return new_intercept




@router.get("/{intercept_id}", response_model=InterceptResponse)
def get_intercept(intercept_id: int, db: Session = Depends(get_db)):
    intercept = db.query(Intercept).filter(Intercept.id == intercept_id).first()
    if not intercept:
        raise HTTPException(status_code=404, detail="Intercept not found")
    return intercept
