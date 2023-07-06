from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
