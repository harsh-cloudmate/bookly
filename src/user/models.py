from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
import uuid
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True),
            default=uuid.uuid4,
            primary_key=True,
            nullable=False
        )
    )

    fname: str = Field(max_length=16, nullable=True)
    lname: str = Field(max_length=16, nullable=True)
    username: str = Field(max_length=20, unique=True)
    email: str
    password_hash: str

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
        return f"<User {self.username}>"