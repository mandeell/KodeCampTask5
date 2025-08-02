from fastapi import HTTPException, FastAPI, Query
from models import Product
from cart import add_to_cart, get_checkout, clear_cart
from storage import read_products, write_products

app = FastAPI(title="Mini Shopping API", description="A simple product and cart management API")

@app.get("/products/")
async def get_products():
    """Get all available products"""
    try:
        products = read_products()
        if not products:
            # Initialize with some sample products if none exist
            sample_products = {
                "1": {"id": 1, "name": "Laptop", "price": 999.99},
                "2": {"id": 2, "name": "Mouse", "price": 25.50},
                "3": {"id": 3, "name": "Keyboard", "price": 75.00},
                "4": {"id": 4, "name": "Monitor", "price": 299.99},
                "5": {"id": 5, "name": "Headphones", "price": 149.99}
            }
            write_products(sample_products)
            products = sample_products
        
        return [Product(**data) for data in products.values()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to retrieve products: {str(e)}')

@app.post("/cart/add")
async def add_to_cart_endpoint(product_id: int = Query(..., description="Product ID to add"), 
                              qty: int = Query(..., description="Quantity to add")):
    """Add a product to the cart with specified quantity"""
    try:
        products = read_products()
        result = add_to_cart(product_id, qty, products)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to add to cart: {str(e)}')

@app.get("/cart/checkout")
async def checkout():
    """Get cart summary and total for checkout"""
    try:
        return get_checkout()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to process checkout: {str(e)}')

@app.delete("/cart/clear")
async def clear_cart_endpoint():
    """Clear all items from the cart"""
    try:
        return clear_cart()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to clear cart: {str(e)}')