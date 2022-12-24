from pydantic import ConstrainedStr, Field

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
        min_length = 1
        max_length = app_config.category_name_length
        to_lower = True
        strip_whitespace = True

    category_name: CategoryName = Field(alias="categoryName")
