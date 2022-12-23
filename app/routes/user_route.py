from fastapi import APIRouter, Depends

from app.models.models import UserModel
from app.schema.user_schema import UserSchema
from app.utils.auth import get_current_user

user_router = APIRouter(tags=["User"])


@user_router.get("/me", response_model=UserSchema)
async def me(current_user: UserModel = Depends(get_current_user)) -> UserSchema:

    return UserSchema(
        user_id=current_user.user_id,
        username=current_user.username,
    )
