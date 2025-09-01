from typing import Self, Unpack
import pydantic

from ycaro_airlines.models.model_database import ModelRepository


class BaseModel(pydantic.BaseModel):
    def __init_subclass__(cls, **kwargs: Unpack[pydantic.ConfigDict]):
        cls.repository = ModelRepository[Self]()
        return super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        self.id: int = self.repository.save(self)
        super().__init__(*args, **kwargs)

    @classmethod
    def get(cls, id: int) -> Self | None:
        return cls.repository.get(id)

    @classmethod
    def list(cls) -> list[Self]:
        return cls.repository.list()
