from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    isActive: bool

class User(UserCreate):
    id: int

    class Config:
        from_attributes = True
