from pydantic import BaseModel


class Immutable(BaseModel):
    class Config:  # noqa: D106 Missing docstring in public nested class
        frozen = True
