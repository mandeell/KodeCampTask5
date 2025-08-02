import json
from pathlib import Path
from fastapi import HTTPException
from math import ceil
from models import Product

DATA_FILE = Path('cart.json')

def read_cart():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted cart.json file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to read cart data: {str(e)}')

def write_cart(cart):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(cart, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to write cart data: {str(e)}')

def add_to_cart(product_id: int, quantity: int, products: dict):
    if product_id not in products:
        raise HTTPException(status_code=404, detail=f'Product {product_id} does not exist')
    if quantity <= 0:
        raise HTTPException(status_code=400, detail=f'Quantity must be greater than 0')

    cart = read_cart()
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'product_id': products[str(product_id)],
            'quantity': quantity,
        }
    write_cart(cart)
    return cart

def get_checkout():
    cart = read_cart()
    if not cart:
        return {'items': [], 'total': 0.0}

    items = []
    total = 0.0

    for product_id, item in cart.items():
        item_total = item['product']['price'] * item['quantity']
        items.append({
            'product': Product(**item['product']),
            'quantity': item['quantity'],
            'item_total': ceil(item_total * 100) / 100,
        })
        total += item_total

        return {
            'items': items,
            'total': ceil(total * 100) / 100,
        }