from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

USERNAME_LENGTH = 64
PASSWORD_HASH_LENGTH = 60

CATEGORY_NAME_LENGTH = 64


class UserModel(Base):
    """User model."""

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(USERNAME_LENGTH), unique=True)
    password_hash: Mapped[str] = mapped_column(String(PASSWORD_HASH_LENGTH))

    categories: Mapped[list["CategoryModel"]] = relationship(back_populates="user")
    expenses: Mapped[list["ExpenseModel"]] = relationship(back_populates="user")


class CategoryModel(Base):
    """Expense category model."""

    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(
        String(CATEGORY_NAME_LENGTH),
        unique=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.user_id))
    user: Mapped["UserModel"] = relationship(back_populates="categories")

    expenses: Mapped[list["ExpenseModel"]] = relationship(back_populates="category")


class ExpenseModel(Base):
    """Expense model."""

    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(primary_key=True)
    expense_amount: Mapped[float] = mapped_column(unique=False)
    expense_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())

    category_id: Mapped[int] = mapped_column(ForeignKey(CategoryModel.category_id))
    category: Mapped["CategoryModel"] = relationship(back_populates="expenses")

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.user_id))
    user: Mapped["UserModel"] = relationship(back_populates="expenses")
