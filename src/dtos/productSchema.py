#DTO's: Data transfer operator used for data validation
from pydantic import BaseModel, EmailStr


class CreateProduct(BaseModel):
    name:str
    price:float = 0.0
    category:str
    stock:int = 0

class UpdateProduct(BaseModel):
    name:str = None
    price:float = None
    category:str = None
    stock:int = None

class orderProduct(BaseModel):
    product_id: int = None
    count: int = None
    mail: EmailStr = None

class userProduct(BaseModel):
    name:str
    email:EmailStr

