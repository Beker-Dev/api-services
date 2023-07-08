from sqlalchemy.orm import Session
from fastapi import UploadFile

from .base import RepositoryBase
from app.database.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate
from app.utils.minio import MinioUtils


class ImageRepository(RepositoryBase[Image, ImageCreate, ImageUpdate]):
    def create(self, db: Session, *, obj_in: ImageCreate, img_file: UploadFile) -> Image:
        obj_in.name = MinioUtils.save_image(img_file)
        return super().create(db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Image, obj_in: ImageUpdate, img_file: UploadFile) -> Image:
        MinioUtils.remove_image(db_obj.image_name)
        obj_in.name = MinioUtils.save_image(img_file)
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: int) -> Image:
        db_img = super().remove(db, id=id)
        MinioUtils.remove_image(db_img.name)
        return db_img


image_repository = ImageRepository(Image)
