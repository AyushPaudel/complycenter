import uuid
from datetime import datetime
from typing import Any
from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    mapped_column,
    registry,
)
from datetime import datetime
from core.config import settings


get_current_time = lambda : datetime.now(tz=settings.timezone)


mapper_registry = registry()


class BaseModel(DeclarativeBase):
    """Base for all models."""

    registry = mapper_registry


@declarative_mixin
class PrimaryUUIDModel(BaseModel):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


@declarative_mixin
class PrimaryTimestampedModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time,
        onupdate=func.now(),
        nullable=False,
    )


@declarative_mixin
class PrimaryUUIDTimestampedModel(PrimaryUUIDModel, PrimaryTimestampedModel):
    __abstract__ = True
