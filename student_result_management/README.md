# Student Result Management System

A FastAPI-based system for managing student academic records with automatic grade calculation and result tracking.

## Features

- **Student Management**: Add and retrieve student records
- **Subject Scores**: Track multiple subject scores per student
- **Automatic Calculations**: Compute average scores and letter grades
- **Data Persistence**: Save student data to JSON file
- **Input Validation**: Comprehensive validation for student data
- **Case-Insensitive Search**: Find students regardless of name case
- **Error Handling**: Robust error handling with detailed messages

## Student Model

### Core Fields
- `name`: String (student name, automatically converted to title case)
- `subject_scores`: Dictionary mapping subject names to scores (0-100)

### Computed Fields
- `average`: Float (automatically calculated from subject scores, rounded to 2 decimal places)
- `grade`: String (letter grade based on average: A, B, C, D, or F)

### Grading Scale
- **A**: 90-100%
- **B**: 80-89%
- **C**: 70-79%
- **D**: 60-69%
- **F**: Below 60%

## API Endpoints

### Create Student
```
POST /students/
```
Create a new student record with subject scores.

### Get Student by Name
```
GET /students/{name}
```
Retrieve a specific student by name (case-insensitive).

### Get All Students
```
GET /students/
```
Retrieve all student records.

## Usage Examples

### 1. Create a Student
```bash
POST /students/
Content-Type: application/json

{
  "name": "john doe",
  "subject_scores": {
    "Mathematics": 85.5,
    "English": 92.0,
    "Science": 78.5,
    "History": 88.0
  }
}
```

**Response:**
```json
{
  "name": "John Doe",
  "subject_scores": {
    "Mathematics": 85.5,
    "English": 92.0,
    "Science": 78.5,
    "History": 88.0
  },
  "average": 86.0,
  "grade": "B"
}
```

### 2. Get Student by Name
```bash
GET /students/john%20doe
GET /students/JOHN%20DOE
GET /students/John%20Doe
```

All variations will find the same student due to case-insensitive matching.

### 3. Get All Students
```bash
GET /students/
```

**Response:**
```json
[
  {
    "name": "John Doe",
    "subject_scores": {
      "Mathematics": 85.5,
      "English": 92.0,
      "Science": 78.5,
      "History": 88.0
    },
    "average": 86.0,
    "grade": "B"
  },
  {
    "name": "Jane Smith",
    "subject_scores": {
      "Mathematics": 95.0,
      "English": 88.5,
      "Science": 91.0
    },
    "average": 91.5,
    "grade": "A"
  }
]
```

## Data Validation

### Student Name
- **Required**: Cannot be empty or whitespace only
- **Normalization**: Automatically converted to title case
- **Example**: `"john doe"` → `"John Doe"`

### Subject Scores
- **Required**: At least one subject score must be provided
- **Score Range**: Each score must be between 0 and 100 (inclusive)
- **Format**: Dictionary with subject names as keys and scores as values
- **Data Type**: Scores must be numeric (int or float)

### Validation Examples

#### Valid Input
```json
{
  "name": "alice johnson",
  "subject_scores": {
    "Math": 95,
    "English": 87.5,
    "Science": 92.0
  }
}
```

#### Invalid Input Examples
```json
// Empty name
{
  "name": "",
  "subject_scores": {"Math": 85}
}

// Score out of range
{
  "name": "Bob Smith",
  "subject_scores": {"Math": 105}
}

// No subject scores
{
  "name": "Carol White",
  "subject_scores": {}
}
```

## File Structure

```
student_result_management/
├── main.py           # FastAPI application with endpoints
├── models.py         # Pydantic models for Student
├── storage.py        # JSON file operations
├── README.md         # This documentation
├── students.json     # Data storage (auto-created)
└── __pycache__/     # Python cache files
```

## Data Storage

### JSON File Format
```json
{
  "John Doe": {
    "name": "John Doe",
    "subject_scores": {
      "Mathematics": 85.5,
      "English": 92.0,
      "Science": 78.5,
      "History": 88.0
    }
  },
  "Jane Smith": {
    "name": "Jane Smith",
    "subject_scores": {
      "Mathematics": 95.0,
      "English": 88.5,
      "Science": 91.0
    }
  }
}
```

### Storage Features
- **File**: `students.json` (created automatically)
- **Format**: Pretty-printed JSON with 2-space indentation
- **Keys**: Student names in title case
- **Persistence**: Data persists between application restarts

## Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (duplicate student)
- `404` - Student not found
- `422` - Validation Error (invalid input data)
- `500` - Internal Server Error

### Error Response Format
```json
{
  "detail": "Descriptive error message"
}
```

### Common Error Scenarios

#### Duplicate Student (400)
```json
{
  "detail": "Student already exists"
}
```

#### Student Not Found (404)
```json
{
  "detail": "Student not found"
}
```

#### Validation Error (422)
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "subject_scores"],
      "msg": "Score for subject Mathematics must be between 0 and 100"
    }
  ]
}
```

#### File Corruption (500)
```json
{
  "detail": "Corrupted students.json file"
}
```

## Grade Calculation Logic

### Average Calculation
```python
average = sum(subject_scores.values()) / len(subject_scores)
average = round(average, 2)  # Rounded to 2 decimal places
```

### Letter Grade Assignment
```python
if average >= 90:
    grade = "A"
elif average >= 80:
    grade = "B"
elif average >= 70:
    grade = "C"
elif average >= 60:
    grade = "D"
else:
    grade = "F"
```

## Running the Application

### Prerequisites
```bash
pip install fastapi uvicorn pydantic
```

### Start the Server
```bash
# Navigate to the project directory
cd student_result_management

# Run with uvicorn
uvicorn main:app --reload --port 8000

# Or run with custom host and port
uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```

### Access the API
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## API Documentation

The FastAPI framework automatically generates interactive API documentation:

### Swagger UI (`/docs`)
- Interactive API explorer
- Test endpoints directly from the browser
- View request/response schemas
- Try out different input combinations

### ReDoc (`/redoc`)
- Clean, readable API documentation
- Detailed endpoint descriptions
- Request/response examples
- Schema definitions

## Technical Implementation

### Pydantic Models
- **BaseModel**: Used for data validation and serialization
- **Field Validators**: Custom validation logic for names and scores
- **Computed Fields**: Automatic calculation of average and grade
- **Type Safety**: Full type hints for better IDE support

### FastAPI Features
- **Automatic Validation**: Request data validated against Pydantic models
- **Error Handling**: Comprehensive try-catch blocks with proper HTTP status codes
- **Documentation**: Auto-generated OpenAPI documentation
- **Type Hints**: Full type annotation support

### File Operations
- **JSON Storage**: Human-readable data format
- **Error Recovery**: Handles file corruption and missing files
- **Atomic Writes**: Safe file writing operations
- **UTF-8 Encoding**: Proper character encoding support

## Example Use Cases

### Academic Institution
- Track student performance across multiple subjects
- Generate report cards with automatic grade calculation
- Monitor class averages and performance trends
- Identify students needing academic support

### Online Learning Platform
- Store quiz and assignment scores
- Calculate course completion grades
- Track learner progress over time
- Generate certificates based on final grades

### Tutoring Service
- Monitor student improvement across sessions
- Track subject-specific performance
- Generate progress reports for parents
- Identify areas needing additional focus

## Features Implemented

✅ **Student Model**: Complete with name and subject scores  
✅ **Automatic Calculations**: Average and grade computation  
✅ **Data Persistence**: JSON file storage  
✅ **Input Validation**: Comprehensive validation rules  
✅ **Case Handling**: Case-insensitive name matching  
✅ **Error Handling**: Robust error handling throughout  
✅ **API Documentation**: Auto-generated interactive docs  
✅ **Type Safety**: Full type hints and validation  
✅ **Grade Scale**: Standard A-F grading system
