from ycaro_airlines_v2.models.base_model import BaseModel


class UserModel(BaseModel):
    username: str
    role: str
    email: str
