from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    price: int
    publication: str
    language: str

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