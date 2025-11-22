from fastapi import APIRouter
from backend.app.drive.sync_service import sync_drive_files

router = APIRouter()

@router.post("/sync")
def sync_route():
    return sync_drive_files()
