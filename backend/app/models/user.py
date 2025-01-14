from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    user_id: Optional[int] = None
    username: str
    email: str
    disabled: Optional[bool] = None
    payment_method: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str 


