from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Float
from .base import PrimaryUUIDTimestampedModel, BaseModel
from sqlalchemy.dialects.postgresql import UUID
from core.config import settings


class User(PrimaryUUIDTimestampedModel):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_role: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Many-to-many via UserBusiness
    businesses: Mapped[list["UserBusiness"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @staticmethod
    def hash_password(raw_password: str):
        return settings.pwd_context.hash(raw_password)

    def check_password(self, raw_password: str):
        return settings.pwd_context.verify(raw_password, self.password)

    def set_password(self, raw_password: str):
        self.password = self.__class__.hash_password(raw_password)


class Business(PrimaryUUIDTimestampedModel):
    __tablename__ = "businesses"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    location_latitude: Mapped[float] = mapped_column(Float, nullable=False)

    location_longitude: Mapped[float] = mapped_column(Float, nullable=False)

    users: Mapped[list["UserBusiness"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    owner_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    email: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    display_picture: Mapped[str | None] = mapped_column(Text, nullable=True)


class UserBusiness(BaseModel):
    __tablename__ = "user_business_association"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    business_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user: Mapped["User"] = relationship(back_populates="businesses")
    business: Mapped["Business"] = relationship(back_populates="users")
