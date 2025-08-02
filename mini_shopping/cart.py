import json
from pathlib import Path
from fastapi import HTTPException
import math
from models import Product

CART_FILE = Path('cart.json')

def read_cart():
    """Read cart data from JSON file"""
    try:
        if CART_FILE.exists():
            with open(CART_FILE, 'r') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted cart.json file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to read cart data: {str(e)}')

def write_cart(cart):
    """Write cart data to JSON file"""
    try:
        with open(CART_FILE, 'w') as f:
            json.dump(cart, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to write cart data: {str(e)}')

def add_to_cart(product_id: int, quantity: int, products: dict):
    """Add a product to the cart with specified quantity"""
    try:
        # Validate product exists
        if str(product_id) not in products:
            raise HTTPException(status_code=404, detail=f'Product with ID {product_id} does not exist')
        
        # Validate quantity
        if quantity <= 0:
            raise HTTPException(status_code=400, detail='Quantity must be greater than 0')

        cart = read_cart()
        product_key = str(product_id)
        
        # Add or update cart item
        if product_key in cart:
            cart[product_key]['quantity'] += quantity
        else:
            cart[product_key] = {
                'product': products[product_key],
                'quantity': quantity
            }
        
        write_cart(cart)
        return {
            'message': f'Added {quantity} of product {product_id} to cart',
            'cart_item': cart[product_key]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to add to cart: {str(e)}')

def get_checkout():
    """Calculate checkout total and return cart summary"""
    try:
        cart = read_cart()
        if not cart:
            return {'items': [], 'total': 0.0, 'item_count': 0}

        items = []
        total = 0.0
        item_count = 0

        for product_id, item in cart.items():
            product_data = item['product']
            quantity = item['quantity']
            item_total = product_data['price'] * quantity
            
            # Use math.ceil for proper rounding to 2 decimal places
            item_total_rounded = math.ceil(item_total * 100) / 100
            
            items.append({
                'product': Product(**product_data),
                'quantity': quantity,
                'item_total': item_total_rounded
            })
            
            total += item_total
            item_count += quantity

        # Round total using math.ceil
        total_rounded = math.ceil(total * 100) / 100

        return {
            'items': items,
            'total': total_rounded,
            'item_count': item_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to process checkout: {str(e)}')

def clear_cart():
    """Clear all items from the cart"""
    try:
        write_cart({})
        return {'message': 'Cart cleared successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to clear cart: {str(e)}')