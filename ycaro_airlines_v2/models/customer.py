from pydantic import Field
from ycaro_airlines_v2.models.user import UserModel


class Customer(UserModel):
    age: int = Field(ge=0, le=130)
    cpf: str = Field(pattern=r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$")

    def __init__(self, **data):
        super().__init__(**data)
