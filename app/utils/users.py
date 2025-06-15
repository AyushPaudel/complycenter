from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
import string
import random

from app.db.models import User
from app.db.dependencies import get_db_session
from app.core.config import settings
from app.services.auth_services import get_active_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/swagger-login")



async def get_current_user(token: str = Depends(oauth2_scheme), session : AsyncSession = Depends(get_db_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
    except jwt.ExpiredSignatureError:
        raise HTTPException(detail="Refresh Token Expired", status_code=400)
    except Exception as e:
        raise HTTPException(detail="Invalid Refresh Token", status_code=400)
    user = await get_active_user(email, session)
    return user


async def is_admin_user(user: User = Depends(get_current_user)):
    """
    Check if the current user has admin privileges.

    Parameters:
    - user: The current user object.

    Returns:
    - True if the user is an admin, otherwise False.
    """
    if user.user_role == "admin":
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to perform this action",
    )

async def generate_password(length=10):
    """Generate a random temporary password"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))
