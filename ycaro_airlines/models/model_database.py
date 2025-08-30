import abc
from itertools import count
from typing import Generic, TypeVar
import pydantic


T = TypeVar("T", bound=pydantic.BaseModel)


class ModelDatabase(abc.ABC, Generic[T]):
    def __init_subclass__(cls) -> None:
        cls.id_counter = count()
        cls.data: dict[int, T | None] = {}
        return super().__init_subclass__()

    @classmethod
    def save(cls, item: T) -> bool:
        item_id = next(cls.id_counter)
        cls.data[item_id] = item
        return True

    @classmethod
    def remove(cls, id: int) -> T | None:
        return cls.data.pop(id)

    @classmethod
    def update(cls, id: int, **kwargs) -> T | None:
        if (item := cls.data.get(id)) is None:
            return None

        model_attribute_dump = item.model_dump()
        model_attribute_dump.update(**kwargs)

        try:
            updated_model: T = T.model_validate(model_attribute_dump)  # pyright: ignore[reportAttributeAccessIssue]

        except pydantic.ValidationError as e:
            print(e)
            return None

        cls.data[id] = updated_model

        return updated_model
