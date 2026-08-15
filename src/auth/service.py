from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .schemas import UserCreate
from sqlmodel import select
from src.utils import hash_password

class AuthService:
    async def get_user_by_uid(self, uid: str, session: AsyncSession):
        user = await session.execute(select(User).where(User.uid == uid))
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str, session: AsyncSession):
        user = await session.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()

    async def register_user(self, user_data: UserCreate, session: AsyncSession):
        password_hash = hash_password(user_data.password)

        new_user = User(
            fname=user_data.fname,
            lname=user_data.lname,
            email=user_data.email,
            password_hash=password_hash
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user