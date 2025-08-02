# Job Application Tracker API

A FastAPI-based system to manage and search job applications with comprehensive error handling and data persistence.

## Features

- **Job Application Management**: Create and track job applications
- **Search Functionality**: Filter applications by status
- **Data Persistence**: Save/load from `applications.json`
- **Error Handling**: Comprehensive try-except blocks throughout
- **Backup System**: Automatic backups before data changes
- **Statistics**: Get insights about your applications

## Models

### JobApplication
- `id`: String (auto-generated from name_company_position)
- `name`: String (applicant name, title case)
- `company`: String (company name, title case)
- `position`: String (job position, title case)
- `status`: Enum (pending, accepted, rejected, interview, withdrawn)

### Status Options
- `pending` - Application submitted, awaiting response
- `accepted` - Application accepted
- `rejected` - Application rejected
- `interview` - Interview scheduled/completed
- `withdrawn` - Application withdrawn

## API Endpoints

### Core Endpoints (Required)
- `POST /applications/` - Create a new job application
- `GET /applications/` - Get all job applications
- `GET /applications/search?status=pending` - Search applications by status

### Additional Endpoints
- `GET /applications/stats` - Get application statistics

## File Structure

```
job_application_tracker/
├── main.py           # FastAPI application with endpoints
├── models.py         # Pydantic models for JobApplication
├── file_handler.py   # JSON file operations module
├── README.md         # This documentation
├── applications.json # Data storage (auto-created)
└── applications.backup.json # Backup file (auto-created)
```

## Usage Examples

### 1. Create a Job Application
```bash
POST /applications/
Content-Type: application/json

{
  "name": "John Doe",
  "company": "Tech Corp",
  "position": "Software Engineer",
  "status": "pending"
}
```

### 2. Get All Applications
```bash
GET /applications/
```

### 3. Search by Status
```bash
GET /applications/search?status=pending
GET /applications/search?status=accepted
GET /applications/search?status=rejected
```

### 4. Get Statistics
```bash
GET /applications/stats
```

## Error Handling

The API implements comprehensive error handling using try-except blocks:

- **File Operations**: Handles JSON corruption, permission errors, file not found
- **Data Validation**: Validates input fields and formats
- **Duplicate Prevention**: Prevents duplicate applications
- **Backup System**: Creates backups before data modifications

## Data Storage

- **Primary Storage**: `applications.json`
- **Backup Storage**: `applications.backup.json` (created automatically)
- **Format**: JSON with UTF-8 encoding
- **Structure**: Dictionary with application IDs as keys

## Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload --port 8000

# Access API documentation
http://localhost:8000/docs
```

## Example Response

### Create Application Response
```json
{
  "id": "john_doe_tech_corp_software_engineer",
  "name": "John Doe",
  "company": "Tech Corp",
  "position": "Software Engineer",
  "status": "pending"
}
```

### Statistics Response
```json
{
  "total": 5,
  "by_status": {
    "pending": 2,
    "accepted": 1,
    "rejected": 1,
    "interview": 1
  },
  "companies": ["Google", "Microsoft", "Tech Corp"]
}
```

## Features Implemented

✅ **JobApplication Class**: Complete with name, company, position, status  
✅ **Required Endpoints**: POST /applications/, GET /applications/, GET /applications/search  
✅ **JSON Persistence**: Save/load from applications.json  
✅ **file_handler.py Module**: Dedicated file operations module  
✅ **Error Handling**: Comprehensive try-except blocks throughout  
✅ **Input Validation**: Pydantic models with field validation  
✅ **Backup System**: Automatic backups before changes  
✅ **Logging**: Detailed logging for debugging and monitoring