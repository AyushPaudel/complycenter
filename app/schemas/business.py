from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class Location(BaseModel):
    latitude: float
    longitude: float


class UserBusiness(BaseModel):
    user_id: str = Field(..., description="ID of the user")
    business_id: str = Field(..., description="ID of the business")

    class Config:
        orm_mode = True


class BusinessBase(BaseModel):
    name: str
    location: Location
    user: Optional[List[UserBusiness]] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    display_picture: Optional[str] = None
    owner_id: Optional[UUID] = None
