
#app = FastAPI(title = "FastAPI", description = "FastAPI crash course")

# def home():
#     return {
#         "message":"Hey! How you doing?"
#     }
from fastapi import FastAPI
from src.routes.product_route import productRoutes
from src.routes.user_route import userRouter

app = FastAPI()


@app.get("/home")
def read_root():
    return {"Hello": "World"}

#CRUD API"S ##JSON file

app.include_router(productRoutes, prefix="/products")
app.include_router(userRouter, prefix="/users")
#using the productRoutes we can include new router
#we already have http://127.0.0.1:8000/home
#http://127.0.0.1:8000/products--> products route has multiple router from productRouter Class
#http://127.0.0.1:8000/products/get-products
##http://127.0.0.1:8000/products/create-products
