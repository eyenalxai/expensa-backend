from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.models.models import UserModel
from app.schema.category_schema import CategorySchema, CategorySchemaAdd
from app.utils.auth import get_current_user
from app.utils.database import get_session
from app.utils.mapper.category_mapper import category_models_to_schemas
from app.utils.query.category_query import (
    add_category,
    get_active_categories,
    get_category_by_id,
    get_category_by_name,
)

category_router = APIRouter(tags=["category"])


@category_router.get("/category", response_model=list[CategorySchema])
async def get(
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> list[CategorySchema]:
    categories = await get_active_categories(
        async_session=async_session,
        user=current_user,
    )

    return category_models_to_schemas(category_models=categories)


@category_router.post("/category")
async def add(
    category_schema: CategorySchemaAdd,
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> Response:
    category = await get_category_by_name(
        async_session=async_session,
        user=current_user,
        category_name=category_schema.category_name,
    )

    if not category:
        add_category(
            async_session=async_session,
            user=current_user,
            category_schema=category_schema,
        )
        return Response(status_code=HTTP_201_CREATED)

    if category.is_active:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="category already added",
        )

    category.is_active = True

    return Response(status_code=HTTP_200_OK)


@category_router.patch("/category/{category_id}")
async def disable(
    category_id: int,
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> Response:
    category = await get_category_by_id(
        async_session=async_session,
        user=current_user,
        category_id=category_id,
    )

    category.is_active = False

    return Response(status_code=HTTP_200_OK)
