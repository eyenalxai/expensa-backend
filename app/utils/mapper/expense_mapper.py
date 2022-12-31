from collections.abc import Sequence

from app.models.models import ExpenseModel
from app.schema.expense_schema import ExpenseSchema
from app.utils.mapper.category_mapper import category_model_to_schema


def expense_model_to_schema(expense_model: ExpenseModel) -> ExpenseSchema:
    return ExpenseSchema(
        expense_id=expense_model.expense_id,
        expense_amount=expense_model.expense_amount,
        expense_date=expense_model.expense_date,
        category=category_model_to_schema(expense_model.category),
    )


def expense_models_to_schemas(
    expense_models: Sequence[ExpenseModel],
) -> list[ExpenseSchema]:
    return [expense_model_to_schema(expense) for expense in expense_models]
