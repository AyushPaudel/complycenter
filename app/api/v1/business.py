from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.business import BusinessBase
from app.db.models import User, Business
from app.db.dependencies import get_db_session
from app.core.logger import get_logger
from app.utils.users import is_admin_user

logger = get_logger("business")


async def create_business(
    business_data: BusinessBase,
    admin_user: User = Depends(is_admin_user),
    session: AsyncSession = Depends(get_db_session),
) -> Business:
    """
    Create a new business.
    Only accessible by admin users.
    """
    query = select(Business).where(Business.name == business_data.name)

    existing_business = await session.execute(query)
    if existing_business.scalar_one_or_none():
        logger.warning(f"Business with name {business_data.name} already exists")
        raise HTTPException(
            status_code=400,
            detail=f"Business with name {business_data.name} already exists",
        )
    business_data.owner_id = admin_user.id

    new_business = Business(**business_data.model_dump())
    session.add(new_business)
    await session.commit()

    logger.info(f"Business {new_business.name} created successfully")
    return new_business


async def get_business(
    business_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> BusinessBase:
    """
    Retrieve a business by its ID.
    """
    query = select(Business).where(Business.id == business_id)
    result = await session.execute(query)
    business = result.scalar_one_or_none()

    if not business:
        logger.error(f"Business with ID {business_id} not found")
        raise HTTPException(status_code=404, detail="Business not found")

    logger.info(f"Business {business.name} retrieved successfully")
    return BusinessBase.model_validate(business)


async def get_all_businesses(
    session: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(is_admin_user),
) -> list[BusinessBase]:
    """
    Retrieve all businesses.
    """
    query = select(Business).where(Business.owner_id == admin_user.id)
    result = await session.execute(query)
    businesses = result.scalars().all()

    if not businesses:
        logger.warning("No businesses found")
        return []

    logger.info(f"Retrieved {len(businesses)} businesses successfully")
    return [BusinessBase.model_validate(business) for business in businesses]


async def update_business(
    business_id: str,
    business_data: BusinessBase,
    admin_user: User = Depends(is_admin_user),
    session: AsyncSession = Depends(get_db_session),
) -> Business:
    """
    Update an existing business.
    Only accessible by admin users.
    """
    query = select(Business).where(Business.id == business_id)
    result = await session.execute(query)
    business = result.scalar_one_or_none()

    if not business:
        logger.error(f"Business with ID {business_id} not found")
        raise HTTPException(status_code=404, detail="Business not found")

    if business.owner_id != admin_user.id:
        logger.error("Unauthorized attempt to update business")
        raise HTTPException(
            status_code=403, detail="Not authorized to update this business"
        )

    for key, value in business_data.model_dump().items():
        setattr(business, key, value)

    await session.commit()
    logger.info(f"Business {business.name} updated successfully")
    return business


async def delete_business(
    business_id: str,
    admin_user: User = Depends(is_admin_user),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """
    Delete a business.
    Only accessible by admin users.
    """
    query = select(Business).where(Business.id == business_id)
    result = await session.execute(query)
    business = result.scalar_one_or_none()

    if not business:
        logger.error(f"Business with ID {business_id} not found")
        raise HTTPException(status_code=404, detail="Business not found")

    if business.owner_id != admin_user.id:
        logger.error("Unauthorized attempt to delete business")
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this business"
        )

    await session.delete(business)
    await session.commit()

    logger.info(f"Business {business.name} deleted successfully")
