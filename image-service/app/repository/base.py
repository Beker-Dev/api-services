from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.config import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def handle_session(func):
    def wrapper(*args, **kwargs):
        response: Any = None

        try:
            response = func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(400, str(e))
        else:
            return response

    return wrapper


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @handle_session
    def get_by_and(self, db: Session, filters: dict) -> Optional[ModelType]:
        filter = []
        for k, v in filters.items():
            if isinstance(v, tuple):
                filter.append(getattr(self.model, k).in_(v))
            else:
                filter.append(getattr(self.model, k) == v)
        return db.query(self.model).filter(*filter)

    @handle_session
    def get_by(self, db: Session, filters: dict) -> Optional[ModelType]:
        return db.query(self.model).filter_by(**filters)

    @handle_session
    def get_by_uuid(self, db: Session, uuid: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == uuid).first()

    @handle_session
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    @handle_session
    def get_or_404(self, db: Session, id: Any) -> Optional[ModelType]:
        db_query = db.query(self.model).filter(self.model.id == id).first()
        if not db_query:
            raise HTTPException(404, f"{self.model.__name__} not found")
        return db_query

    @handle_session
    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    @handle_session
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @handle_session
    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @handle_session
    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
