from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/ingest")

@router.post("")
async def ingest(file: UploadFile = File(...)):
    # Dummy: just return filename
    return {"filename": file.filename, "status": "received"}
