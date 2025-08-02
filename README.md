# KodeCampTask5 - FastAPI Applications Collection

A comprehensive collection of FastAPI applications demonstrating various web development concepts, data management techniques, and API design patterns.

## 🚀 Project Overview

This repository contains **5 distinct FastAPI applications**, each showcasing different aspects of modern web API development:

1. **Student Result Management System** - Academic record management with automatic grade calculation
2. **Mini Shopping API** - E-commerce cart and product management system
3. **Job Application Tracker** - Job search and application status management
4. **Notes App** - File-based note management system
5. **Simple Contact App** - Contact management with in-memory storage

## 📁 Project Structure

```
KodeCampTask5/
├── student_result_management/    # Academic records management
│   ├── main.py                  # FastAPI app with student endpoints
│   ├── models.py                # Student model with grade calculation
│   ├── storage.py               # JSON file operations
│   ├── README.md                # Detailed documentation
│   └── students.json            # Student data storage
│
├── mini_shopping/               # E-commerce shopping system
│   ├── main.py                  # FastAPI app with product/cart endpoints
│   ├── models.py                # Product model
│   ├── cart.py                  # Cart management logic
│   ├── storage.py               # File operations
│   ├── README.md                # Detailed documentation
│   ├── products.json            # Product catalog
│   └── cart.json                # Shopping cart data
│
├── job_application_tracker/     # Job application management
│   ├── main.py                  # FastAPI app with application endpoints
│   ├── models.py                # Job application models
│   ├── file_handler.py          # File operations with backup
│   ├── README.md                # Detailed documentation
│   └── applications.json        # Application data storage
│
├── notes_app/                   # File-based note management
│   ├── main.py                  # FastAPI app with note endpoints
│   ├── models.py                # Note models with validation
│   ├── file_handler.py          # OS module file operations
│   ├── README.md                # Detailed documentation
│   └── notes/                   # Directory for note files
│       ├── note1.txt
│       └── note2.txt
│
├── simple_contact_app/          # Contact management system
│   ├── main.py                  # FastAPI app with contact endpoints
│   ├── models.py                # Contact models with validation
│   └── README.md                # Detailed documentation
│
├── .venv/                       # Python virtual environment
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🛠️ Technologies Used

### Core Technologies
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running FastAPI applications
- **Python 3.8+** - Programming language

### Data Storage
- **JSON Files** - Lightweight data persistence
- **In-Memory Dictionary** - Runtime data storage
- **File System** - Text file storage for notes

### Development Tools
- **Git** - Version control
- **GitHub** - Remote repository hosting
- **Virtual Environment** - Isolated Python environment
- **Logging** - Application monitoring and debugging

## 🎯 Application Features

### 1. Student Result Management System
**Purpose**: Manage student academic records with automatic grade calculation

**Key Features**:
- ✅ Student registration with multiple subject scores
- ✅ Automatic average calculation (rounded to 2 decimal places)
- ✅ Letter grade assignment (A, B, C, D, F)
- ✅ Case-insensitive student lookup
- ✅ JSON data persistence

**Endpoints**:
- `POST /students/` - Create student record
- `GET /students/{name}` - Get student by name
- `GET /students/` - Get all students

### 2. Mini Shopping API
**Purpose**: E-commerce product browsing and cart management

**Key Features**:
- ✅ Product catalog management
- ✅ Shopping cart functionality
- ✅ Add/remove items with quantities
- ✅ Checkout with total calculation
- ✅ Math module for price rounding

**Endpoints**:
- `GET /products/` - Browse products
- `POST /cart/add?product_id=1&qty=2` - Add to cart
- `GET /cart/checkout` - Calculate totals
- `DELETE /cart/clear` - Clear cart

### 3. Job Application Tracker
**Purpose**: Track job applications and search status

**Key Features**:
- ✅ Job application management (name, company, position, status)
- ✅ Status filtering (pending, accepted, rejected, interview, withdrawn)
- ✅ Comprehensive search functionality
- ✅ Automatic backup system
- ✅ Statistics and analytics

**Endpoints**:
- `POST /applications/` - Create application
- `GET /applications/` - Get all applications
- `GET /applications/search?status=pending` - Search by status
- `GET /applications/stats` - Get statistics

### 4. Notes App
**Purpose**: File-based note management system

**Key Features**:
- ✅ Create, read, update, delete notes
- ✅ Each note saved as individual .txt file
- ✅ OS module for file operations
- ✅ File metadata tracking (size, timestamps)
- ✅ Comprehensive error handling

**Endpoints**:
- `POST /notes/` - Create note
- `GET /notes/{title}` - Get note
- `POST /notes/{title}` - Update note
- `DELETE /notes/{title}` - Delete note

### 5. Simple Contact App
**Purpose**: Contact management with in-memory storage

**Key Features**:
- ✅ Contact model (name, phone, email)
- ✅ Path and query parameters
- ✅ In-memory dictionary storage
- ✅ Input validation and sanitization
- ✅ Case-insensitive contact search

**Endpoints**:
- `POST /contacts/` - Create contact
- `GET /contacts/?name=John` - Search contacts
- `POST /contacts/{name}` - Update contact
- `DELETE /contacts/{name}` - Delete contact

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Git (for cloning)
git --version
```

### Installation
```bash
# Clone the repository
git clone https://github.com/mandeell/KodeCampTask5.git
cd KodeCampTask5

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydantic
```

### Running Applications

Each application can be run independently:

#### Student Result Management
```bash
cd student_result_management
uvicorn main:app --reload --port 8001
# Access: http://localhost:8001/docs
```

#### Mini Shopping API
```bash
cd mini_shopping
uvicorn main:app --reload --port 8002
# Access: http://localhost:8002/docs
```

#### Job Application Tracker
```bash
cd job_application_tracker
uvicorn main:app --reload --port 8003
# Access: http://localhost:8003/docs
```

#### Notes App
```bash
cd notes_app
uvicorn main:app --reload --port 8004
# Access: http://localhost:8004/docs
```

#### Simple Contact App
```bash
cd simple_contact_app
uvicorn main:app --reload --port 8005
# Access: http://localhost:8005/docs
```

## 📚 API Documentation

Each application provides interactive API documentation:

- **Swagger UI**: `http://localhost:PORT/docs`
- **ReDoc**: `http://localhost:PORT/redoc`
- **OpenAPI Schema**: `http://localhost:PORT/openapi.json`

## 🧪 Testing the APIs

### Using Swagger UI (Recommended)
1. Navigate to the `/docs` endpoint for any application
2. Explore available endpoints
3. Test requests directly in the browser
4. View request/response schemas

### Using cURL
```bash
# Create a student
curl -X POST "http://localhost:8001/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "subject_scores": {"Math": 85, "English": 92}}'

# Add item to cart
curl -X POST "http://localhost:8002/cart/add?product_id=1&qty=2"

# Create job application
curl -X POST "http://localhost:8003/applications/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Smith", "company": "Tech Corp", "position": "Developer", "status": "pending"}'
```

### Using Python Requests
```python
import requests

# Test student API
response = requests.post("http://localhost:8001/students/", json={
    "name": "Alice Johnson",
    "subject_scores": {"Math": 95, "Science": 88}
})
print(response.json())
```

## 🔧 Development Features

### Error Handling
- ✅ Comprehensive try-catch blocks
- ✅ Proper HTTP status codes
- ✅ Detailed error messages
- ✅ Input validation with Pydantic

### Data Validation
- ✅ Type checking with Pydantic models
- ✅ Custom field validators
- ✅ Automatic data sanitization
- ✅ Format validation (email, phone, etc.)

### Logging
- ✅ Application-level logging
- ✅ Error tracking and debugging
- ✅ Operation monitoring
- ✅ Performance insights

### Code Quality
- ✅ Type hints throughout
- ✅ Docstring documentation
- ✅ Modular architecture
- ✅ Separation of concerns

## 📊 Data Storage Patterns

### JSON File Storage
- **Applications**: Student Management, Shopping, Job Tracker
- **Benefits**: Human-readable, version control friendly
- **Use Case**: Persistent data that survives restarts

### In-Memory Dictionary
- **Applications**: Contact Management
- **Benefits**: Fast access, simple implementation
- **Use Case**: Session-based data, rapid prototyping

### File System Storage
- **Applications**: Notes App
- **Benefits**: Individual file management, OS integration
- **Use Case**: Document management, content storage

## 🛡️ Security Considerations

### Input Validation
- All user inputs validated with Pydantic models
- SQL injection prevention through parameterized queries
- XSS protection through input sanitization

### Error Handling
- Sensitive information not exposed in error messages
- Proper HTTP status codes for different scenarios
- Graceful degradation on failures

### File Operations
- Path traversal protection in file operations
- Safe filename handling and sanitization
- Proper file permissions and access control

## 🚀 Deployment Options

### Local Development
```bash
# Run with auto-reload for development
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Production Deployment
```bash
# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for functions
- Maintain consistent naming conventions

## 📈 Future Enhancements

### Potential Features
- **Authentication & Authorization**: JWT-based user authentication
- **Database Integration**: PostgreSQL/MongoDB support
- **Caching**: Redis caching for improved performance
- **Testing**: Comprehensive test suites with pytest
- **Monitoring**: Application metrics and health checks
- **API Versioning**: Support for multiple API versions
- **Rate Limiting**: Request throttling and abuse prevention
- **Documentation**: Enhanced API documentation with examples

### Scalability Improvements
- **Microservices Architecture**: Split into independent services
- **Message Queues**: Async processing with Celery/RQ
- **Load Balancing**: Multiple instance deployment
- **CDN Integration**: Static asset optimization

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

### Getting Help
- **Documentation**: Check individual app README files
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

### Contact Information
- **Repository**: [https://github.com/mandeell/KodeCampTask5](https://github.com/mandeell/KodeCampTask5)
- **Author**: mandeell

## 🎯 Learning Objectives

This project demonstrates:

1. **FastAPI Fundamentals**: Building REST APIs with FastAPI
2. **Data Modeling**: Using Pydantic for data validation
3. **File Operations**: Different data storage approaches
4. **Error Handling**: Robust error management strategies
5. **API Design**: RESTful endpoint design principles
6. **Documentation**: Auto-generated API documentation
7. **Project Structure**: Organizing multi-application projects
8. **Version Control**: Git workflow and repository management

## 🏆 Achievements

- ✅ **5 Complete Applications** - Fully functional FastAPI apps
- ✅ **Comprehensive Documentation** - Detailed README files for each app
- ✅ **Error Handling** - Robust error management throughout
- ✅ **Data Validation** - Input validation with Pydantic models
- ✅ **Multiple Storage Patterns** - JSON, in-memory, and file system storage
- ✅ **Interactive Documentation** - Auto-generated API docs
- ✅ **Version Control** - Git repository with proper structure
- ✅ **Modular Design** - Clean separation of concerns

---

**Happy Coding! 🚀**