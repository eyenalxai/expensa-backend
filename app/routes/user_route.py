from fastapi import APIRouter, Depends

from app.models.models import UserModel
from app.schema.user_schema import UserSchema
from app.utils.auth import get_current_user
from app.utils.mapper.user_mapper import user_model_to_schema

user_router = APIRouter(tags=["User"])


@user_router.get("/me", response_model=UserSchema)
async def me(current_user: UserModel = Depends(get_current_user)) -> UserSchema:
    return user_model_to_schema(user=current_user)
