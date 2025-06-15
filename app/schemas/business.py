from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class Location(BaseModel):
    latitude: float
    longitude: float


class BusinessBase(BaseModel):
    name: str
    location: Location
    user: Optional[List[UUID]] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    display_picture: Optional[str] = None
    owner_id: Optional[UUID] = None
