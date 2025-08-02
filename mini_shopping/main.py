from fastapi import HTTPException, FastAPI, Query
from models import Product
from cart import add_to_cart, get_checkout
from storage import read_products

app = FastAPI()

@app.get("/products")
async def get_products():
    products = read_products()
    return [Product(**data) for data in products.values()]

@app.get("/cart/add")
async def add_to_cart_endpoint(product_id: int = Query(...), quantity: int = Query(...)):
    products = read_products()
    cart = add_to_cart(product_id, quantity, products)
    return cart

@app.get("/cart/checkout")
async def checkout():
    return get_checkout()