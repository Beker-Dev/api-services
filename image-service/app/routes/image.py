from fastapi import APIRouter, Depends, UploadFile, File, Response
from typing import Any, Optional
from PIL import Image
import os
from datetime import datetime

from app.schemas.image import ImageCreate, ImageUpdate, ImageShow


router = APIRouter(tags=['Image'], prefix='/images')


@router.post("", response_model=Any)
async def upload_image(
        image_file: UploadFile = File(...)
):
    image_object = get_image_object(image_file)
    return Response(image_object, 201)


def get_image_object(file: UploadFile):
    name, extension = os.path.splitext(file.filename)
    size = file.size
    img = Image.open(file.file)
    width, height = img.size
    resolution = f"{width}x{height}"
    bits = img.bits

    image_object = {
        "name": name,
        "extension": extension,
        "resolution": resolution,
        "width": width,
        "height": height,
        "size": size,
        "bits": bits,
        "is_active": True,
        "uploaded_at": "",
        "modified_at": None,
        "accessed_at": None,
        "removed_at": None
    }
    return str(image_object)
