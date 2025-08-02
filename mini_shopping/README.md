# Mini Shopping API

A simple FastAPI-based product and cart management system that allows users to browse products, add items to cart, and checkout.

## Features

- **Product Management**: Browse available products
- **Cart Operations**: Add products to cart with quantities
- **Checkout**: Calculate totals with proper rounding using math module
- **Data Persistence**: Save cart data to JSON file
- **Error Handling**: Comprehensive error handling throughout

## API Endpoints

### Products
- `GET /products/` - Get all available products

### Cart Operations
- `POST /cart/add?product_id=1&qty=2` - Add product to cart
- `GET /cart/checkout` - Get cart summary and total
- `DELETE /cart/clear` - Clear all items from cart

## Models

### Product
- `id`: Integer (positive)
- `name`: String (non-empty)
- `price`: Float (positive, rounded to 2 decimal places)

## Data Storage

- Products: `products.json`
- Cart: `cart.json`

## Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload --port 8000

# Access API documentation
http://localhost:8000/docs
```

## Example Usage

1. **Get Products**:
   ```
   GET /products/
   ```

2. **Add to Cart**:
   ```
   POST /cart/add?product_id=1&qty=2
   ```

3. **Checkout**:
   ```
   GET /cart/checkout
   ```

## Math Module Usage

The application uses Python's `math` module for proper price rounding:
- `math.ceil()` is used to round prices up to the nearest cent
- Ensures accurate financial calculations

## Version Control

This project uses Git for version tracking and is connected to GitHub for remote repository management.