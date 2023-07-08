from fastapi import APIRouter, Depends, UploadFile, File
from typing import Any, Optional
from PIL import Image
from datetime import datetime
from sqlalchemy.orm import Session
import os

from app.schemas.image import ImageCreate, ImageUpdate, ImageShow
from app.repository.image import image_repository
from app.core import dependencies as deps


router = APIRouter(tags=['Image'], prefix='/images')


@router.post("", response_model=ImageShow)
async def upload_image(
        db: Session = Depends(deps.get_db),
        image_file: UploadFile = File(...)
):
    image_object = get_image_object(image_file)
    return image_repository.create(db=db, obj_in=image_object, img_file=image_file)


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
    }
    return ImageCreate(**image_object)
