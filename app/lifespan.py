from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import ssl 

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.db.models import User
from app.schemas.users import UserRole


ssl_context = ssl.create_default_context(cafile="app/ca.pem")


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), connect_args={"ssl": ssl_context},
    echo=settings.DB_ECHO,)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


@asynccontextmanager
async def lifespan_setup(app: FastAPI) -> AsyncGenerator[None, None]:
    app.middleware_stack = None
    _setup_db(app)
    app.middleware_stack = app.build_middleware_stack()

    # # Create admin user if not exists
    async with app.state.db_session_factory() as session:
        await create_admin_user_if_not_exists(session)

    yield
    await app.state.db_engine.dispose()


async def create_admin_user_if_not_exists(session: AsyncSession) -> None:
    result = await session.execute(
        select(User).where(User.email == "admin@complycenter.com")
    )
    admin_user = result.scalar_one_or_none()

    if not admin_user:
        admin = User(
            email="admin@complycenter.com",
            full_name="admin",
            password=User.hash_password("AdminPassword123!"),
            user_role=UserRole.ADMIN,
        )
        session.add(admin)
        await session.commit()
        print("✅ Admin user created")
    else:
        print("ℹ️ Admin user already exists")
