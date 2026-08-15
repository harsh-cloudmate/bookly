from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    uid: str
    fname: str
    lname: str
    role: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    email: str
    password: str