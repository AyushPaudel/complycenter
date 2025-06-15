from pydantic import BaseModel, EmailStr, field_serializer
from enum import Enum
import uuid


class UserRole(str, Enum):
    """
    Enum for user roles.
    Defines the different roles a user can have in the system.
    """

    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    CLEANER = "cleaner"


class CreateUser(BaseModel):   
    full_name: str 
    email: EmailStr 
    user_role: UserRole



class ReturnUser(BaseModel):
    """
    Base model for user schemas.
    Contains common fields for user-related operations.
    """
    id : uuid.UUID 
    full_name: str 
    email: EmailStr 
    user_role: UserRole

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
