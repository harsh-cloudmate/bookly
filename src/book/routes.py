from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException
from .schema import Book, BookCreationPayload, BookUpdationPayload
from typing import List
from .book_data import Books as raw_books

book_router = APIRouter()

Books = [Book(**book) for book in raw_books]

@book_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Book])
def get_books() -> List[Book]:
    return Books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
def add_book(payload: BookCreationPayload) -> Book:
    id = len(Books) + 1

    new_book = Book(
        id = id,
        **payload.model_dump()
    )

    Books.append(new_book)

    return new_book

@book_router.patch("/{book_id}", status_code=status.HTTP_201_CREATED, response_model=Book)
def update_book(book_id: int, payload: BookUpdationPayload) -> Book:

    for book in Books:
        if book.id == book_id:
            update_data = payload.model_dump(exclude_unset=True)

            updated_book = book.model_copy(update=update_data)

            Books[Books.index(book)] = updated_book

            return updated_book

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_book(book_id: int):
    global Books

    for book in Books:
        if book.id == book_id:
            Books = list(filter(lambda b: b.id != book_id, Books))

            return {}

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")