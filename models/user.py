from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

USERNAME_LENGTH = 64
PASSWORD_HASH_LENGTH = 512


class UserModel(Base):
    """User model."""

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(USERNAME_LENGTH), unique=True)
    password_hash: Mapped[str] = mapped_column(String(PASSWORD_HASH_LENGTH))
