from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    price: int
    publication: str
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreationPayload(BaseModel):
    title: str
    author: str
    price: int
    publication: str
    language: str

class BookUpdationPayload(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[int] = None
    publication: Optional[str] = None
    language: Optional[str] = None