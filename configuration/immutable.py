from pydantic import BaseModel


class Immutable(BaseModel):
    """Makes pydantic models immutable."""

    class Config:  # noqa: D106 Missing docstring in public nested class

        frozen = True
