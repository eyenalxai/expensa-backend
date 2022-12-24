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
    add_user_category,
    delete_user_category_by_id,
    get_user_categories,
    is_category_already_added,
)

category_router = APIRouter(tags=["Category"], prefix="/category")


@category_router.get("/", response_model=list[CategorySchema])
async def get_categories(
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> list[CategorySchema]:
    categories = await get_user_categories(
        async_session=async_session,
        user=current_user,
    )

    return category_models_to_schemas(category_models=categories)


@category_router.post("/")
async def add_category(
    category: CategorySchemaAdd,
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> Response:
    is_already_added = await is_category_already_added(
        async_session=async_session,
        user=current_user,
        category_name=category.category_name,
    )

    if is_already_added:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="category already added",
        )

    add_user_category(
        async_session=async_session,
        user=current_user,
        category=category,
    )

    return Response(status_code=HTTP_201_CREATED)


@category_router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> Response:
    await delete_user_category_by_id(
        async_session=async_session,
        user=current_user,
        category_id=category_id,
    )

    return Response(status_code=HTTP_200_OK)
