from fastapi import APIRouter, HTTPException
from src.utils.utils import get_all_users
from typing import List
from src.dtos.productSchema import userProduct
userRouter = APIRouter()

@userRouter.get("/",response_model=List[userProduct])
def get_alluser():
    allUsers = get_all_users()
    return allUsers