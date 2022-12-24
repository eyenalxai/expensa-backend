from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import CategoryModel, UserModel
from app.schema.category_schema import CategorySchemaAdd


async def get_user_categories(
    async_session: AsyncSession,
    user: UserModel,
) -> Sequence[CategoryModel]:
    query = select(CategoryModel).where(CategoryModel.user == user)
    query_result = await async_session.execute(query)

    return query_result.scalars().all()


def add_user_category(
    async_session: AsyncSession,
    user: UserModel,
    category: CategorySchemaAdd,
) -> None:
    category_model = CategoryModel(
        category_name=category.category_name,
        user=user,
    )

    async_session.add(category_model)


async def delete_user_category_by_id(
    async_session: AsyncSession,
    user: UserModel,
    category_id: int,
) -> None:
    category_query = delete(CategoryModel).where(
        CategoryModel.user == user,
        CategoryModel.category_id == category_id,
    )

    await async_session.execute(category_query)


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
