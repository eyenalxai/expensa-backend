from collections.abc import Sequence

from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import CategoryModel, UserModel
from app.schema.category_schema import CategorySchemaAdd


async def get_active_categories(
    async_session: AsyncSession,
    user: UserModel,
) -> Sequence[CategoryModel]:
    query = select(CategoryModel).where(
        CategoryModel.user == user,
        CategoryModel.is_active == true(),
    )
    query_result = await async_session.execute(query)

    return query_result.scalars().all()


async def get_category_by_id(
    async_session: AsyncSession,
    user: UserModel,
    category_id: int,
) -> CategoryModel:
    query = select(CategoryModel).where(
        CategoryModel.user == user,
        CategoryModel.category_id == category_id,
    )
    query_result = await async_session.execute(query)

    return query_result.scalar_one()


async def get_category_by_name(
    async_session: AsyncSession,
    user: UserModel,
    category_name: str,
) -> CategoryModel | None:
    query = select(CategoryModel).where(
        CategoryModel.user == user,
        CategoryModel.category_name == category_name,
    )
    query_result = await async_session.execute(query)

    return query_result.scalar_one_or_none()


def add_category(
    async_session: AsyncSession,
    user: UserModel,
    category_schema: CategorySchemaAdd,
) -> None:
    category_model = CategoryModel(
        category_name=category_schema.category_name,
        user=user,
    )

    async_session.add(category_model)


async def is_category_already_added(
    async_session: AsyncSession,
    user: UserModel,
    category_name: str,
) -> bool:
    query = select(CategoryModel).where(
        CategoryModel.user == user,
        CategoryModel.category_name == category_name,
    )
    query_result = await async_session.execute(query)

    return query_result.scalar_one_or_none() is not None
