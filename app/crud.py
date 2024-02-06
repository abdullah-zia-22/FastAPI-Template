from app.schemas import UserCreate
from app.models import User
from sqlalchemy import exc, or_,func
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import Base
from app.security import get_password_hash


#Base Class for CRUDs
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_multi(
        self, db: Session, *, limit: int = 10, offset: int = 0,search: Optional[str] = None
    ) -> List[ModelType]:
            return db.query(self.model).offset(offset).limit(limit).all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        return db_obj

    async def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    


#API Key Model CRUDs
class CRUDUser(CRUDBase[User, UserCreate]):
    async def create(self, db: Session, *, obj_in: UserCreate):
        try:
            db_obj = User(
                email=obj_in.email,
                password=get_password_hash(obj_in.password),
                username=obj_in.username,
                isActive=obj_in.isActive
            )
            db.add(db_obj)
            db.commit()
        except exc.IntegrityError:
            db.rollback()
            return None

    async def update(self, db: Session, *, db_obj: User, obj_in: UserCreate):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        return db_obj
    
    async def get_user_by_email(self, db: Session, *, email: str) -> Any:
        email = email.lower()
        resp = db.query(self.model).filter(or_(func.lower(self.model.email) == email, func.lower(self.model.username)==email)).first()
        return resp
    
    async def authenticate(
        self, db: Session, *, email: str
    ) -> Optional[User]:
        user = await self.get_user_by_email(db, email=email)
        return user
    
    async def get_all(self, db: Session, *, search: Optional[str] = None) -> List[UserCreate]: 
        query = db.query(self.model)
    
        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    self.model.email.ilike(search_term),
                    self.model.username.ilike(search_term),
                )
            )

        return query.all()  




#Object creation
user = CRUDUser(User)