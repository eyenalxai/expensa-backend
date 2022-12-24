from app.models.models import UserModel
from app.schema.user_schema import UserSchema


def user_model_to_schema(user: UserModel) -> UserSchema:
    return UserSchema(
        user_id=user.user_id,
        username=user.username,
    )
