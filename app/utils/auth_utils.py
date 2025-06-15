from pydantic import BaseModel
from datetime import timedelta, datetime
from passlib.context import CryptContext
import jwt
from core.config import settings
from db.models import User



def create_access_token(user : User) -> str:
    """
    Returns JWT encoded access string of the input

    Parameters:
    data -- dictionary which contains the user_name

    Returns:
    encoded_jwt -- string value
    """
    to_encode = {"email": user.email, "user_role": user.user_role}
    expire = datetime.now(tz=settings.timezone) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(user : User) -> str:
    """
    Creates JWT encoded refresh string of the input

    Parameters:
    data -- dictionary which contains the user_name, role

    Returns:
    encoded_jwt -- string value
    """
    to_encode = {"email": user.email, "user_role": user.user_role}
    expire = datetime.now(tz=settings.timezone) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), settings.ALGORITHM
    )

    return encoded_jwt
