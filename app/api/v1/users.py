from fastapi import Depends

from app.utils.users import get_current_user
from app.db.models import User
from app.core.logger import get_logger

logger = get_logger("users")


# Todo: get assigned businesses
async def get_profile(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
