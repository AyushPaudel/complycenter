from fastapi import APIRouter
from schemas.users import ReturnUser, Token
from .auth import invite_user, swagger_login, get_token, refresh_token
from .users import get_profile
from .business import (
    create_business,
    get_business,
    get_all_businesses,
    update_business,
    delete_business,
)
from schemas.business import BusinessBase

v1router = APIRouter(prefix="/api/v1")

# Auth
v1router.add_api_route(
    "/swagger-login",
    endpoint=swagger_login,
    methods=["POST"],
    include_in_schema=False,
    response_model=Token,
)

v1router.add_api_route(
    "/users",
    endpoint=invite_user,
    methods=["POST"],
    tags=["Admin"],
    response_model=ReturnUser,
)

v1router.add_api_route(
    "/token", endpoint=get_token, methods=["POST"], tags=["Auth"], response_model=Token
)
v1router.add_api_route(
    "/token/refresh",
    endpoint=refresh_token,
    methods=["POST"],
    tags=["Auth"],
    response_model=Token,
)

# Users
v1router.add_api_route(
    "/profile",
    endpoint=get_profile,
    methods=["GET"],
    tags=["User"],
    response_model=ReturnUser,
)


# Business
v1router.add_api_route(
    "/businesses",
    endpoint=create_business,
    methods=["POST"],
    tags=["Business"],
    response_model=BusinessBase,
)

v1router.add_api_route(
    "/businesses/{business_id}",
    endpoint=get_business,
    methods=["GET"],
    tags=["Business"],
    response_model=BusinessBase,
)

v1router.add_api_route(
    "/businesses",
    endpoint=get_all_businesses,
    methods=["GET"],
    tags=["Business"],
    response_model=list[BusinessBase],
)
v1router.add_api_route(
    "/businesses/{business_id}",
    endpoint=update_business,
    methods=["PUT"],
    tags=["Business"],
    response_model=BusinessBase,
)
v1router.add_api_route(
    "/businesses/{business_id}",
    endpoint=delete_business,
    methods=["DELETE"],
    tags=["Business"],
    response_model=None,
)
