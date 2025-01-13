# from fastapi import APIRouter, Depends, UploadFile, HTTPException
# from sqlalchemy.orm import Session
# from server.db import models, database
# from server.services.minio_service import upload_file_to_minio
# from server.schemas.file import FileCreate, FileResponse
# from server.core.config import settings

# router = APIRouter()

# @router.post("/upload", response_model=FileResponse)
# def upload_file(file: UploadFile, db: Session = Depends(database.get_db)):
#     try:
#         file_data = file.file.read()
#         url = upload_file_to_minio(settings.MINIO_BUCKET_NAME, file.filename, file_data)
#         new_file = models.FileRecord(filename=file.filename, url=url)
#         db.add(new_file)
#         db.commit()
#         db.refresh(new_file)
#         return new_file
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

# @router.get("/files/{file_id}", response_model=FileResponse)
# def get_file(file_id: int, db: Session = Depends(database.get_db)):
#     file_record = db.query(models.FileRecord).filter(models.FileRecord.id == file_id).first()
#     if not file_record:
#         raise HTTPException(status_code=404, detail="File not found")
#     return file_record

