from configuration.immutable import Immutable


class User(Immutable):
    """
    User data transfer object.

    Attributes:
        user_id (int): User ID.
        username (str): Username.
    """

    class Config:  # noqa: D106 Missing docstring in public nested class
        orm_mode = True

    user_id: int
    username: str
