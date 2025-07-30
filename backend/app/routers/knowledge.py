from fastapi import APIRouter, UploadFile, File, Depends
from ..auth import get_current_user, User

knowledge_router = APIRouter(prefix="/kb")

@knowledge_router.post("/upload")
async def upload_kb(file: UploadFile = File(...), _: User = Depends(get_current_user)):
    # placeholder
    return {"msg": f"received {file.filename}"}
