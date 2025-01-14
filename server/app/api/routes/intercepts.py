from app.services.minio_service import upload_to_minio
from app.core.config import settings

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from sqlalchemy.orm import Session
from common.schemas.intercept import (
    InterceptCreateRequest,
    InterceptCreateResponse,
    InterceptAudioCreate
)
from app.db.database import get_db
from app.db.models import Intercept, InterceptAudioFile, Node
import json


router = APIRouter(
    prefix="/intercepts",
    tags=["intercepts"]
)

"""
we are using mult-part form data to send the json request along with a file upload
but this means the json data is encoded into a field
"""

@router.post("/", response_model=InterceptCreateResponse)
async def publish_intercept(
        request: InterceptCreateRequest,
        db: Session = Depends(get_db)
    ):

    print(f"#### request = {request}")

    # Resolve the ID if only the name is provided
    if not request.node_id:
        node = db.query(Node).filter(Node.name == request.node_name).first()
        if not node:
            raise HTTPException(status_code=404, detail=f"Node with name '{request.node_name}' not found.")
        node_id = node.id
    else:
        node_id = request.node_id

    print(f"#### node_id = {node_id}")

    # Create an Intercept instance
    db_intercept = Intercept(
        node_id=node_id,
        time_start=request.time_start,
        duration=request.duration,
        frequency_center=request.frequency_center
    )

    # Insert into the database
    db.add(db_intercept)
    db.commit()
    db.refresh(db_intercept)  # Fetch the updated object with its ID

    # Return the created intercept
    print(f"db_intercept.id = {db_intercept.id}")
    return InterceptCreateResponse(
        id=db_intercept.id
    )

        # # parsing and validation of request
        # intercept = json.loads(intercept)
        # req = InterceptCreate(**intercept)

        # # Read the file contents
        # file_data = await file.read()

        # mio = upload_to_minio(settings.MINIO_BUCKET_NAME, file.filename, file_data)

        # new_intercept = Intercept(
        #     **intercept,
        #     audio_file = InterceptAudioFile(
        #         bucket_name=mio.bucket_name,
        #         object_name=mio.object_name,
        #         etag=mio.etag,
        #         size=len(file_data)
        #     )
        # )

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

    #     db.add(new_intercept)
    #     db.commit()
    #     db.refresh(new_intercept)

    #     return req
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"create_intercept failed: {e}")


    # new_intercept = Intercept(**intercept.dict())
    # db.add(new_intercept)
    # db.commit()
    # db.refresh(new_intercept)
    # return new_intercept




# @router.get("/{intercept_id}", response_model=InterceptResponse)
# def get_intercept(intercept_id: int, db: Session = Depends(get_db)):
#     intercept = db.query(Intercept).filter(Intercept.id == intercept_id).first()
#     if not intercept:
#         raise HTTPException(status_code=404, detail="Intercept not found")
#     return intercept
