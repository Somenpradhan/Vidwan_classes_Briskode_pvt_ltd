import os
import uuid
import shutil
from fastapi import UploadFile
from app.core.config import settings


UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class StorageService:
    @staticmethod
    async def save_file(file: UploadFile, folder: str = "media") -> str:
        """
        Save uploaded file according to configured STORAGE_PROVIDER.
        Default: Local filesystem storage with public static URL.
        """
        provider = settings.STORAGE_PROVIDER.lower()
        
        if provider == "local":
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            target_folder = os.path.join(UPLOAD_DIR, folder)
            os.makedirs(target_folder, exist_ok=True)
            file_path = os.path.join(target_folder, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Return accessible URL route
            return f"{settings.BACKEND_URL}/uploads/{folder}/{filename}"
        
        # Extensible placeholder for Supabase / Cloudinary / S3
        else:
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            target_folder = os.path.join(UPLOAD_DIR, folder)
            os.makedirs(target_folder, exist_ok=True)
            file_path = os.path.join(target_folder, filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return f"{settings.BACKEND_URL}/uploads/{folder}/{filename}"


storage_service = StorageService()
