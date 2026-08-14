from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from src.book.models import Book
from src.book.schema import BookCreationPayload, BookUpdationPayload


class BookService:
    async def get_all_books(self, session: AsyncSession):
        result = await session.execute(select(Book).order_by(desc(Book.created_at)))

        return result.scalars().all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        result = await session.execute(select(Book).where(Book.uid == book_uid))

        if result is None:
            return None

        return result.scalar_one_or_none()

    async def add_book(self, book_data: BookCreationPayload, session: AsyncSession):
        book_payload = book_data.model_dump()

        new_book = Book(
            **book_payload
        )

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(self, book_uid: str, book_data: BookUpdationPayload, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is None:
            return None

        updated_book = book_data.model_dump(exclude_unset=True)

        for k, v in updated_book.items():
            setattr(book_to_update, k, v)

        await session.commit()

        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is None:
            return None

        await session.delete(book_to_delete)

        await session.commit()

        return {}