from fastapi import APIRouter, HTTPException
from src.utils.utils import get_all_products, create_all_products, simple_send
from src.dtos.productSchema import CreateProduct, UpdateProduct,orderProduct
from fastapi import BackgroundTasks

productRoutes = APIRouter()

#Normal product fetch and Query param implementation
@productRoutes.get("/")
def get_allProducts(product_id: int | None = None):
    all_Products = get_all_products()
    if product_id is None:
        return all_Products
    
    for product in all_Products:
        if product["id"] == product_id:   
            return product
    raise HTTPException(status_code=404, detail={"error": "product_id not found"})

#Path Param implementation
@productRoutes.get("/{id}")
def get_oneProduct(id:int):
    all_Products = get_all_products()
    for product in all_Products:
        if product["id"] == id:

            return product
    raise HTTPException(status_code=400, detail={"error":"id not found"})#{"message":"Not found"}

    
#Path Param:
#ex for path param:http://127.0.0.1:8000/products/12
#passing the id dynamically directly in the path
#Query Param:
#ex for query param:http://127.0.0.1:8000/products?id = 12 & price = 10
@productRoutes.post("/create")
def create_product(product:CreateProduct):
    products = get_all_products()
    product = product.model_dump()#This was in object form need to convert to dictionary file
    p_id = max([p["id"] for p in products])+1
    product["id"] = p_id
    products.append(product) #we need to store this new data in the file/db
    create_all_products(products)
    return {"message":"New Product created successfully"}

#Update
@productRoutes.put("/update/{id}")
def update_product(product:UpdateProduct, id:int = None):
    if not id:
        raise HTTPException(status_code=400, detail={"error":"Product_id must be passed"})

    allProducts = get_all_products()
    for index, p in enumerate(allProducts):
        if p["id"] ==id:
            changes = {}
            for k,v in product.model_dump().items():
                if v is not None:
                    changes[k] = v
            allProducts[index] = {"id":id,**p,**changes}
            create_all_products(allProducts)
            return {"message":"Product updated successfully"}

#Delete

@productRoutes.delete("/delete/{id}")
def update_product(product:UpdateProduct, id:int = None):
    if not id:
        raise HTTPException(status_code=400, detail={"error":"Product_id must be passed"})

    allProducts = get_all_products()
    for index, p in enumerate(allProducts):
        if p["id"] ==id:
            allProducts.pop(index)
           
            create_all_products(allProducts)
            return {"message":"Product deleted successfully"}


@productRoutes.post("/order")
async def place_order(order:orderProduct ,bgTask:BackgroundTasks):

    count = order.count
    product_id = order.product_id
    email = order.mail

    if not product_id:
        raise HTTPException(status_code=400, detail={"error":"Product_id must be passed"})
    allProducts = get_all_products()
    oneProduct = None
    for index, p in enumerate(allProducts):
        if p["id"] == product_id:
            oneProduct = p
            break
    if not oneProduct:
        raise HTTPException(status_code=400, detail={"error":"product_id not found"})

    if oneProduct["stock"] < count:
        raise HTTPException(status_code=400, detail={"error":"Product is out of stock"})

    bgTask.add_task(simple_send,email)

    return {"message":"Order placed successfully"}