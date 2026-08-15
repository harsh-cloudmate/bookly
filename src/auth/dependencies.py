from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from .service import AuthService
from src.db.main import get_session
from src.utils import decode_jwt_token
from datetime import datetime

auth_service = AuthService()

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, session: AsyncSession = Depends(get_session)) -> User:
        credentials = await super().__call__(request)

        token = credentials.credentials if credentials else None
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            if not token:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

        decoded_token = decode_jwt_token(token)

        await self.verify_jwt(decoded_token)

        user = await auth_service.get_user_by_uid(decoded_token.get("uid"), session)

        return user

    async def verify_jwt(self, decoded_token: dict | None):
        raise NotImplementedError("Subclasses must implement the verify_jwt method.")

class AssessTokenBearer(JWTBearer):
    async def verify_jwt(self, decoded_token: dict | None):
        if datetime.fromtimestamp(decoded_token.get("exp")) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
        
        if decoded_token.get("refresh") == True:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type. Access token required.")

class RefreshTokenBearer(JWTBearer):
    async def verify_jwt(self, decoded_token: dict | None):
        if datetime.fromtimestamp(decoded_token.get("exp")) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
        
        if decoded_token.get("refresh") == False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type. Refresh token required.")
