from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schema import Book, BookCreationPayload, BookUpdationPayload
from .service import BookService
from typing import List

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await book_service.get_all_books(session)

    return result

@book_router.get("/{book_uid}", status_code=status.HTTP_200_OK, response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    result = await book_service.get_book(book_uid, session)

    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")

    return result

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def add_book(payload: BookCreationPayload, session: AsyncSession = Depends(get_session)):
    result = await book_service.add_book(payload, session)

    return result

@book_router.patch("/{book_uid}", status_code=status.HTTP_201_CREATED, response_model=Book)
async def update_book(book_uid: str, payload: BookUpdationPayload, session: AsyncSession = Depends(get_session)):

    result = await book_service.update_book(book_uid, payload, session)

    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")

    return result

@book_router.delete("/{book_uid}", status_code=status.HTTP_202_ACCEPTED)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):

    result = await book_service.delete_book(book_uid, session)

    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")

    return result