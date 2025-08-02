# Notes API

A FastAPI application to add, update, and delete notes saved as individual text files using the `os` module with comprehensive error handling.

## Features

- **File-based Storage**: Each note is saved as a separate `.txt` file
- **CRUD Operations**: Create, read, update, and delete notes
- **OS Module Integration**: Uses Python's `os` module for file operations
- **Error Handling**: Comprehensive try-except blocks throughout
- **File Metadata**: Track file size, creation time, and modification time
- **Input Validation**: Sanitize note titles for filesystem compatibility

## API Endpoints

### Required Endpoints
- `POST /notes/` - Create a new note
- `GET /notes/{title}` - Get a note by title
- `POST /notes/{title}` - Update an existing note
- `DELETE /notes/{title}` - Delete a note

### Additional Endpoints
- `GET /notes/` - List all notes with metadata
- `GET /` - API information and usage

## Models

### NoteCreate
- `title`: String (sanitized for filesystem compatibility)
- `content`: String (note content)

### Note (Response Model)
- `title`: String (note title)
- `content`: String (note content)
- `file_path`: String (path to the .txt file)
- `file_size`: Integer (file size in bytes)
- `created_at`: String (ISO format timestamp)
- `modified_at`: String (ISO format timestamp)

### NoteUpdate
- `content`: String (new content for the note)

## File Structure

```
notes_app/
├── main.py           # FastAPI application with endpoints
├── models.py         # Pydantic models
├── file_handler.py   # File operations using os module
├── README.md         # This documentation
└── notes/           # Directory for note files (auto-created)
    ├── note1.txt
    ├── note2.txt
    └── ...
```

## Usage Examples

### 1. Create a Note
```bash
POST /notes/
Content-Type: application/json

{
  "title": "My First Note",
  "content": "This is the content of my first note."
}
```

**Response:**
```json
{
  "title": "My First Note",
  "content": "This is the content of my first note.",
  "file_path": "notes/My First Note.txt",
  "file_size": 42,
  "created_at": "2024-01-15T10:30:00",
  "modified_at": "2024-01-15T10:30:00"
}
```

### 2. Get a Note
```bash
GET /notes/My First Note
```

### 3. Update a Note
```bash
POST /notes/My First Note
Content-Type: application/json

{
  "content": "This is the updated content of my note."
}
```

### 4. Delete a Note
```bash
DELETE /notes/My First Note
```

**Response:**
```json
{
  "message": "Note 'My First Note' deleted successfully",
  "deleted_file": "notes/My First Note.txt"
}
```

### 5. List All Notes
```bash
GET /notes/
```

**Response:**
```json
{
  "notes": [
    {
      "title": "My First Note",
      "file_size": 42,
      "created_at": "2024-01-15T10:30:00",
      "modified_at": "2024-01-15T10:30:00"
    }
  ],
  "total_count": 1,
  "notes_directory": "notes"
}
```

## OS Module Usage

The application extensively uses Python's `os` module for file operations:

- `os.makedirs()` - Create the notes directory
- `os.path.exists()` - Check if note files exist
- `os.stat()` - Get file metadata (size, timestamps)
- `os.remove()` - Delete note files
- File operations with proper encoding (`utf-8`)

## Error Handling

Comprehensive error handling using try-except blocks:

### File Operations
- **FileNotFoundError**: When trying to read/update non-existent notes
- **PermissionError**: When lacking file system permissions
- **OSError**: General file system errors

### HTTP Status Codes
- `201` - Note created successfully
- `200` - Operation successful
- `404` - Note not found
- `409` - Note already exists (conflict)
- `403` - Permission denied
- `500` - Internal server error

### Error Response Format
```json
{
  "detail": "Descriptive error message"
}
```

## Input Validation

### Title Sanitization
- Removes invalid filename characters: `< > : " / \ | ? *`
- Replaces them with underscores
- Limits length to 100 characters
- Ensures non-empty titles

### Content Validation
- Allows empty content (for blank notes)
- Validates against `None` values
- Preserves original formatting

## File Storage Details

- **Directory**: `notes/` (created automatically)
- **File Format**: `.txt` files with UTF-8 encoding
- **Naming**: `{sanitized_title}.txt`
- **Content**: Raw text content as provided

## Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload --port 8000

# Access API documentation
http://localhost:8000/docs
```

## Features Implemented

✅ **Required Endpoints**: All specified endpoints implemented  
✅ **Text File Storage**: Each note saved as individual .txt file  
✅ **OS Module Usage**: Extensive use of os module for file operations  
✅ **Error Handling**: Comprehensive try-except blocks throughout  
✅ **Input Validation**: Title sanitization and content validation  
✅ **File Metadata**: Track file size and timestamps  
✅ **Directory Management**: Automatic creation of notes directory  
✅ **Logging**: Detailed logging for debugging and monitoring

## Security Considerations

- **Path Traversal Protection**: Title sanitization prevents directory traversal
- **File Extension Control**: Only `.txt` files are created
- **Input Validation**: Prevents malicious input
- **Error Information**: Detailed but safe error messages