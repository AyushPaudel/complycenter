from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import Token, UserLogin, CreateUser
from services.auth_services import create_user, authenticate_user, get_user
from utils.auth_utils import create_access_token, create_refresh_token
from db.models import User
from db.dependencies import get_db_session
import jwt
from core.config import settings
from core.logger import get_logger
from utils.users import is_admin_user

logger = get_logger("auth")

# TODO: Send email notification to the invited user with id, password
# Todo: Add password reset link


async def invite_user(
    user_data: CreateUser,
    admin_user: User = Depends(is_admin_user),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    try:
        await get_user(user_data.email, session)
    except HTTPException:
        created_user = await create_user(user_data.model_dump(), session)
        return created_user
    logger.warning(f"User with email {user_data.email} already registered")
    raise HTTPException(
        status_code=400, detail=f"User with email {user_data.email} already registered"
    )


async def swagger_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db_session),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    logger.info(f"User with email {user.email} signed in successfully")
    return Token(
        **{
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user),
            "token_type": "bearer",
        }
    )


async def get_token(data: UserLogin, session: AsyncSession = Depends(get_db_session)):
    user = await authenticate_user(data.email, data.password, session)
    logger.info(f"User with email {user.email} signed in successfully")
    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }


async def refresh_token(
    refresh_token: str, session: AsyncSession = Depends(get_db_session)
):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("email")
    except jwt.ExpiredSignatureError as e:
        logger.debug(f"Refresh Token Expired: {str(e)}")
        raise HTTPException(detail="Refresh Token Expired", status_code=400)
    except Exception as e:
        logger.debug(f"Unable to refresh token: {str(e)}")
        raise HTTPException(detail="Invalid Refresh Token", status_code=400)

    user = await get_user(email, session)
    return {"access_token": create_access_token(user)}
