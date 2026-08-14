from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from datetime import datetime, timezone
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True),
            default=uuid.uuid4,
            primary_key=True,
            nullable=False
        )
    )
    
    title: str
    author: str
    price: int
    publication: str
    language: str

    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=lambda : datetime.now(timezone.utc),
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=lambda : datetime.now(timezone.utc),
            onupdate=lambda : datetime.now(timezone.utc),
            nullable=False
        )
    )

    def __repr__(self):
        return f"<Book {self.title}>"