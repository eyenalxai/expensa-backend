from collections.abc import Sequence

from app.models.models import CategoryModel
from app.schema.category_schema import CategorySchema


def category_model_to_schema(category_model: CategoryModel) -> CategorySchema:
    return CategorySchema(
        category_id=category_model.category_id,
        category_name=category_model.category_name,
    )


def category_models_to_schemas(
    category_models: Sequence[CategoryModel],
) -> list[CategorySchema]:
    return [category_model_to_schema(category) for category in category_models]
