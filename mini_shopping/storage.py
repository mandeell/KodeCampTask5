# storage.py
import json
from pathlib import Path
from fastapi import HTTPException

PRODUCTS_FILE = Path('products.json')

def read_products():
    try:
        if PRODUCTS_FILE.exists():
            with open(PRODUCTS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted products.json file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read products data: {str(e)}")

def write_products(products):
    try:
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(products, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write products data: {str(e)}")