from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from app.utils.minio import MinioUtils

class ImageBase(BaseModel):
    name: str = Field(max_length=100)
    extension: str = Field(max_length=5)
    resolution: str = Field(max_length=10)
    width: int
    height: int
    size: int
    bits: int


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class ImageShow(ImageBase):
    id: UUID
    url: Optional[str]
    thumb: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    def dict(self, **kwargs):
        self.url = MinioUtils.get_image(self.name)
        self.thumb = MinioUtils.get_image('thumb_' + self.name)
        return super().dict(**kwargs)

    class Config:
        orm_mode = True
