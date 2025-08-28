from fastapi import APIRouter, UploadFile, Form, File
from app.s3_utils import upload_avatar
from app.db_utils import save_user, get_all_users

router = APIRouter()

@router.get("/users")
async def list_users():
    return get_all_users()

@router.post("/user")
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    avatar: UploadFile = File(...)
):
    avatar_url = upload_avatar(avatar)
    save_user(name, email, avatar_url)
    return {"name": name, "email": email, "avatar_url": avatar_url}

