from configuration.immutable import Immutable


class User(Immutable):
    class Config:  # noqa: D106 Missing docstring in public nested class
        orm_mode = True

    user_id: int
    username: str
