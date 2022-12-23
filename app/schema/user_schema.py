from app.utils.immutable import Immutable


class UserSchema(Immutable):
    class Config:
        orm_mode = True

    user_id: int
    username: str
