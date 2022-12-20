from fastapi import APIRouter, Depends

from dto.user import User
from lib.auth.authenticate import get_current_user
from models.user import UserModel

user_router = APIRouter(tags=["User"])


@user_router.get("/me", response_model=User)
async def me(current_user: UserModel = Depends(get_current_user)) -> User:
    """
    Get current user.

    Args:
        current_user (UserModel): Current user. Injected as dependency.

    Returns:
        User: User dto.

    """
    return User(
        user_id=current_user.user_id,
        username=current_user.username,
    )
