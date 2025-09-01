from enum import Enum
from ycaro_airlines.models.base_model import BaseModel


class Roles(Enum):
    CustomerService = "Worker"
    Customer = "Customer"


class User(BaseModel):
    username: str
    email: str
    role: Roles | None = None

    def __init__(self, username: str, *args, **kwargs) -> None:
        super().__init__(username=username, *args, **kwargs)
