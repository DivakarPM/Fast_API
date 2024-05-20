from pydantic import BaseModel, Field
from typing import Optional,Dict


class User(BaseModel):
    user_id: int
    username: str

class UserManager:
    def __init__(self):
        self.data_dict: Dict[int, str] = {1: "Divakar", 2: "John", 3: "Shiv"}

    def get_user(self, user_id: int) -> User:
        username = self.data_dict.get(user_id)
        if username:
            return User(user_id=user_id, username=username)
        else:
            return None


# Tow types of declaring optional fields
class Product(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    tax : float | None = None
    itempresent : bool | None = None


class Diabetes(BaseModel):
    Pregnancies	: int
    Glucose	: float
    BloodPressure : float	
    SkinThickness : float
    Insulin	: float
    BMI	: float
    DiabetesPedigreeFunction : float
    Age	: int
    poduct : Product

class DiabetesExample(Diabetes):
    Pregnancies: int = Field(default=2, example=2)
    Glucose: float = Field(default=120, example=120.0)
    BloodPressure: float = Field(default=70, example=70.0)
    SkinThickness: float = Field(default=35, example=35.0)
    Insulin: float = Field(default=0, example=0.0)
    BMI: float = Field(default=33.6, example=33.6)
    DiabetesPedigreeFunction: float = Field(default=0.627, example=0.627)
    Age: int = Field(default=50, example=50)

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []