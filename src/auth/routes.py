from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .models import User
from .service import AuthService
from .schemas import UserCreate
from src.utils import verify_password, create_jwt_token
from .dependencies import AssessTokenBearer, RefreshTokenBearer

auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await auth_service.get_user_by_email(user_data.email, session)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    user = await auth_service.register_user(user_data, session)
    return user

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await auth_service.get_user_by_email(user_data.email, session)
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_jwt_token({"uid": str(user.uid), "email": user.email, "role": user.role}, refresh=False)
    refresh_token = create_jwt_token({"uid": str(user.uid), "email": user.email, "role": user.role}, refresh=True)

    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "user": user.json()}, status_code=status.HTTP_200_OK)

@auth_router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(user: User = Depends(AssessTokenBearer())):
    return user

@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(user: User = Depends(RefreshTokenBearer())):
    access_token = create_jwt_token({"uid": str(user.uid), "email": user.email, "role": user.role}, refresh=False)
    return JSONResponse(content={"access_token": access_token}, status_code=status.HTTP_200_OK)