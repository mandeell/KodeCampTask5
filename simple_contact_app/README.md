# Contact Management System

A FastAPI-based contact management system that uses path and query parameters, stores data in an in-memory dictionary, and handles invalid input gracefully.

## Features

- **Contact Model**: name, phone, email
- **In-Memory Storage**: Data stored in Python dictionary
- **Path Parameters**: Contact operations using URL paths
- **Query Parameters**: Filtering contacts by name
- **Input Validation**: Graceful handling of invalid input
- **CRUD Operations**: Create, read, update, and delete contacts

## Contact Model

### Fields
- `name`: String (required, normalized to title case)
- `phone`: String (required, 7-15 digits in various formats)
- `email`: String (required, valid email format)

### Validation Rules
- **Name**: Cannot be empty, automatically converted to title case
- **Phone**: Must contain 7-15 digits, supports various formats (e.g., "123-456-7890", "(123) 456-7890", "+1234567890")
- **Email**: Must be valid email format, automatically converted to lowercase

## API Endpoints

### Required Endpoints
- `POST /contacts/` - Create a new contact
- `GET /contacts/?name=John` - Get contacts with optional name filter (query parameter)
- `POST /contacts/{name}` - Update a contact completely (path parameter)
- `DELETE /contacts/{name}` - Delete a contact (path parameter)

### Additional Endpoints
- `PATCH /contacts/{name}` - Partially update a contact
- `GET /contacts/stats` - Get contact statistics
- `GET /` - API information

## Usage Examples

### 1. Create a Contact
```bash
POST /contacts/
Content-Type: application/json

{
  "name": "john doe",
  "phone": "123-456-7890",
  "email": "JOHN@EXAMPLE.COM"
}
```

**Response:**
```json
{
  "name": "John Doe",
  "phone": "123-456-7890",
  "email": "john@example.com"
}
```

### 2. Get All Contacts
```bash
GET /contacts/
```

### 3. Filter Contacts by Name (Query Parameter)
```bash
GET /contacts/?name=John
GET /contacts/?name=john
GET /contacts/?name=Jo
```

### 4. Update Contact (Path Parameter)
```bash
POST /contacts/John Doe
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "987-654-3210",
  "email": "john.doe@newdomain.com"
}
```

### 5. Partially Update Contact
```bash
PATCH /contacts/John Doe
Content-Type: application/json

{
  "phone": "555-123-4567"
}
```

### 6. Delete Contact (Path Parameter)
```bash
DELETE /contacts/John Doe
```

**Response:**
```json
{
  "message": "Contact 'John Doe' deleted successfully",
  "deleted_contact": "John Doe"
}
```

## Path and Query Parameters

### Path Parameters
- Used in endpoints like `/contacts/{name}`
- Contact name is extracted from the URL path
- Example: `/contacts/John%20Doe` for contact named "John Doe"

### Query Parameters
- Used for filtering: `/contacts/?name=John`
- Optional parameter for searching contacts
- Supports partial name matching (case-insensitive)

## Data Storage

### In-Memory Dictionary
```python
contacts_db: Dict[str, Dict[str, Any]] = {
    "John Doe": {
        "name": "John Doe",
        "phone": "123-456-7890",
        "email": "john@example.com"
    },
    "Jane Smith": {
        "name": "Jane Smith", 
        "phone": "987-654-3210",
        "email": "jane@example.com"
    }
}
```

### Key Features
- **Normalized Keys**: Contact names stored in title case
- **Case-Insensitive Lookup**: Searches work regardless of input case
- **In-Memory Only**: Data persists only during application runtime

## Invalid Input Handling

### Validation Errors (422)
```json
{
  "detail": "Name cannot be empty"
}
```

### Conflict Errors (409)
```json
{
  "detail": "Contact with name 'John Doe' already exists"
}
```

### Not Found Errors (404)
```json
{
  "detail": "Contact 'John Doe' not found"
}
```

### Server Errors (500)
```json
{
  "detail": "Failed to create contact: unexpected error"
}
```

## Input Validation Examples

### Valid Phone Formats
- `"123-456-7890"`
- `"(123) 456-7890"`
- `"+1234567890"`
- `"123.456.7890"`
- `"1234567890"`

### Invalid Phone Examples
- `"123"` (too short)
- `"12345678901234567890"` (too long)
- `"abc-def-ghij"` (no digits)

### Valid Email Examples
- `"user@example.com"`
- `"test.email@domain.org"`
- `"user+tag@example.co.uk"`

### Invalid Email Examples
- `"invalid-email"`
- `"@example.com"`
- `"user@"`

## Error Handling Features

### Graceful Input Handling
- **Validation Errors**: Clear messages for invalid data
- **Duplicate Prevention**: Prevents creating duplicate contacts
- **Not Found Handling**: Proper 404 responses for missing contacts
- **Server Error Recovery**: Catches unexpected errors

### Logging
- **Info Logging**: Successful operations logged
- **Error Logging**: Detailed error information for debugging
- **Operation Tracking**: All CRUD operations tracked

## Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload --port 8000

# Access API documentation
http://localhost:8000/docs
```

## API Documentation

Once running, access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Features Implemented

✅ **Contact Model**: name, phone, email with validation  
✅ **Required Endpoints**: All specified endpoints implemented  
✅ **Path Parameters**: Contact operations using URL paths  
✅ **Query Parameters**: Name filtering with query params  
✅ **Dictionary Storage**: In-memory dictionary storage  
✅ **Invalid Input Handling**: Comprehensive error handling  
✅ **Input Validation**: Phone and email format validation  
✅ **Case Normalization**: Consistent name handling  
✅ **Partial Updates**: PATCH endpoint for partial updates  
✅ **Statistics**: Contact statistics endpoint

## Technical Details

### Storage Implementation
- **Type**: In-memory Python dictionary
- **Key Format**: Normalized contact names (title case)
- **Value Format**: Contact data as dictionary
- **Persistence**: Data lost on application restart

### Parameter Handling
- **Path Parameters**: Extracted using FastAPI `Path()` 
- **Query Parameters**: Extracted using FastAPI `Query()`
- **Validation**: Automatic validation with Pydantic models
- **Documentation**: Auto-generated parameter documentation