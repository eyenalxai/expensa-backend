from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED

from app.models.models import UserModel
from app.schema.expense_schema import ExpenseSchema, ExpenseSchemaAdd
from app.utils.auth import get_current_user
from app.utils.database import get_session
from app.utils.mapper.expense_mapper import expense_models_to_schemas
from app.utils.query.category_query import get_category_by_id
from app.utils.query.expense_query import add_expense, get_expenses

expense_router = APIRouter(tags=["expense"])


@expense_router.get("/expense", response_model=list[ExpenseSchema])
async def get(
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> list[ExpenseSchema]:
    expenses = await get_expenses(
        async_session=async_session,
        user=current_user,
    )

    return expense_models_to_schemas(expense_models=expenses)


@expense_router.post("/expense")
async def add(
    expense_schema: ExpenseSchemaAdd,
    async_session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> Response:
    category = await get_category_by_id(
        async_session=async_session,
        user=current_user,
        category_id=expense_schema.category_id,
    )

    await add_expense(
        async_session=async_session,
        user=current_user,
        category=category,
        expense_amount=expense_schema.expense_amount,
    )

    return Response(status_code=HTTP_201_CREATED)
