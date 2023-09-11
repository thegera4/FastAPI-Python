from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Product(s) not found"}})

products_list = ["prod1", "prod2", "prod3", "prod4", "prod5"]


@router.get("/")
async def products():
    return products_list


@router.get("/{product_id}")
async def product(product_id: int):
    try:
        return products_list[product_id]
    except IndexError:
        return {"message": "Product not found."}
