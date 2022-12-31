from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.models import CategoryModel, ExpenseModel, UserModel


async def get_expenses(
    async_session: AsyncSession,
    user: UserModel,
) -> Sequence[ExpenseModel]:
    query = (
        select(ExpenseModel)
        .where(ExpenseModel.user == user)
        .options(joinedload(ExpenseModel.category))
    )

    query_result = await async_session.execute(query)

    return query_result.scalars().all()


async def get_expenses_by_category(
    async_session: AsyncSession,
    user: UserModel,
    category: CategoryModel,
) -> Sequence[ExpenseModel]:
    query = select(ExpenseModel).where(
        ExpenseModel.user == user,
        ExpenseModel.category == category,
    )
    query_result = await async_session.execute(query)

    return query_result.scalars().all()


async def add_expense(
    async_session: AsyncSession,
    user: UserModel,
    category: CategoryModel,
    expense_amount: float,
) -> None:
    expense_model = ExpenseModel(
        expense_amount=expense_amount,
        category=category,
        user=user,
    )

    async_session.add(expense_model)


async def delete_expense_by_id(
    async_session: AsyncSession,
    user: UserModel,
    expense_id: int,
) -> None:
    query = delete(ExpenseModel).where(
        ExpenseModel.user == user,
        ExpenseModel.expense_id == expense_id,
    )

    await async_session.execute(query)
