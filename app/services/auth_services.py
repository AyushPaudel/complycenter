from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import User
from db.dependencies import get_db_session
from pydantic import EmailStr


async def create_user(
    user_data: dict,
    session: AsyncSession,
):
    user_data["password"] = User.hash_password("defaultpassword")
    db_user = User(**user_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user(email: EmailStr, session: AsyncSession):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(detail=f"No user found with email {email}", status_code=400)
    return user


async def get_active_user(email: EmailStr, session: AsyncSession):
    query = select(User).where(User.email == email, User.is_active == True)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(detail=f"No active user found with email {email}", status_code=401)
    return user


async def authenticate_user(
    email: str,
    password: str,
    session : AsyncSession
):
    user = await get_active_user(email, session)
    if not user.check_password(password):
        raise HTTPException(detail="Invalid Credentials", status_code=400)
    return user



