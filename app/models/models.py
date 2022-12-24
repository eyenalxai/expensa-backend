from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config_reader import app_config
from app.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(app_config.username_length),
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(String(app_config.password_hash_length))

    categories: Mapped[list["CategoryModel"]] = relationship(back_populates="user")
    expenses: Mapped[list["ExpenseModel"]] = relationship(back_populates="user")


class CategoryModel(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(
        String(app_config.category_name_length),
        unique=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.user_id))
    user: Mapped["UserModel"] = relationship(back_populates="categories")

    expenses: Mapped[list["ExpenseModel"]] = relationship(back_populates="category")


class ExpenseModel(Base):
    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(primary_key=True)
    expense_amount: Mapped[float] = mapped_column(unique=False)
    expense_date: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())

    category_id: Mapped[int] = mapped_column(ForeignKey(CategoryModel.category_id))
    category: Mapped["CategoryModel"] = relationship(back_populates="expenses")

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.user_id))
    user: Mapped["UserModel"] = relationship(back_populates="expenses")
