from pydantic import ConstrainedStr, Field, validator

from app.config.config_reader import app_config
from app.utils.immutable import Immutable


class CategorySchema(Immutable):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    category_id: int = Field(alias="categoryId")
    category_name: str = Field(alias="categoryName")


class CategorySchemaAdd(Immutable):
    class CategoryName(ConstrainedStr):
        to_lower = True
        strip_whitespace = True

    category_name: CategoryName = Field(alias="categoryName")

    @validator("category_name")
    def category_name_must_be_ok(
        cls,  # noqa: N805 first argument of a method should be named 'self'
        v: str,  # noqa: WPS111 Found too short name: v < 2
    ) -> str:
        if len(v) < 1:  # noqa: WPS507 Found useless `len()` compare
            raise ValueError("category name is too short")

        if len(v) > app_config.category_name_length:
            raise ValueError("category name is too long")

        return v
