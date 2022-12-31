from datetime import datetime

from pydantic import ConstrainedStr, Field

from app.schema.category_schema import CategorySchema
from app.utils.immutable import Immutable


class ExpenseSchema(Immutable):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    expense_id: int = Field(alias="expenseId")
    expense_amount: float = Field(alias="expenseAmount")
    expense_date: datetime = Field(alias="expenseDate")

    category: CategorySchema


class ExpenseSchemaAdd(Immutable):
    class CategoryName(ConstrainedStr):
        to_lower = True
        strip_whitespace = True

    expense_amount: float = Field(alias="expenseAmount")
    category_id: int = Field(alias="categoryId")
