# main.py
from fastapi import FastAPI, HTTPException, Query, Path
from models import ContactCreate, Contact, ContactUpdate
from typing import List, Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Contact Management System",
    description="FastAPI contact management system with path and query parameters",
    version="1.0.0"
)

# In-memory dictionary to store contacts
contacts_db: Dict[str, Dict[str, Any]] = {}

def normalize_name(name: str) -> str:
    """
    Normalize name for consistent storage and lookup.
    
    Args:
        name: Contact name
        
    Returns:
        Normalized name in title case
    """
    return name.strip().title()

def find_contact_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Find a contact by name (case-insensitive).
    
    Args:
        name: Contact name to search for
        
    Returns:
        Contact data if found, None otherwise
    """
    normalized_name = normalize_name(name)
    return contacts_db.get(normalized_name)

@app.post("/contacts/", status_code=201, response_model=Contact)
async def create_contact(contact: ContactCreate):
    """
    Create a new contact.
    
    Args:
        contact: Contact data with name, phone, and email
        
    Returns:
        Created contact
        
    Raises:
        HTTPException: If contact creation fails or contact already exists
    """
    try:
        normalized_name = normalize_name(contact.name)
        
        # Check if contact already exists
        if normalized_name in contacts_db:
            raise HTTPException(
                status_code=409, 
                detail=f"Contact with name '{normalized_name}' already exists"
            )
        
        # Store contact in dictionary
        contact_data = contact.model_dump()
        contacts_db[normalized_name] = contact_data
        
        logger.info(f"Created contact: {normalized_name}")
        return Contact(**contact_data)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error creating contact: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create contact: {str(e)}"
        )

@app.get("/contacts/", response_model=List[Contact])
async def get_contacts(name: Optional[str] = Query(None, description="Filter contacts by name")):
    """
    Get contacts with optional name filter using query parameter.
    
    Args:
        name: Optional name filter (query parameter)
        
    Returns:
        List of contacts (filtered by name if provided)
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        if name is None:
            # Return all contacts
            result = [Contact(**data) for data in contacts_db.values()]
            logger.info(f"Retrieved all {len(result)} contacts")
            return result
        
        # Filter by name (case-insensitive partial match)
        normalized_search = normalize_name(name)
        filtered_contacts = []
        
        for contact_name, contact_data in contacts_db.items():
            if normalized_search.lower() in contact_name.lower():
                filtered_contacts.append(Contact(**contact_data))
        
        logger.info(f"Found {len(filtered_contacts)} contacts matching '{name}'")
        return filtered_contacts
        
    except Exception as e:
        logger.error(f"Error retrieving contacts: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve contacts: {str(e)}"
        )

@app.post("/contacts/{name}", response_model=Contact)
async def update_contact_full(
    name: str = Path(..., description="Contact name to update"),
    contact: ContactCreate = None
):
    """
    Update a contact completely using POST method with path parameter.
    
    Args:
        name: Contact name (path parameter)
        contact: New contact data
        
    Returns:
        Updated contact
        
    Raises:
        HTTPException: If contact not found or update fails
    """
    try:
        normalized_name = normalize_name(name)
        
        # Check if contact exists
        if normalized_name not in contacts_db:
            raise HTTPException(
                status_code=404, 
                detail=f"Contact '{normalized_name}' not found"
            )
        
        # Update contact data
        contact_data = contact.model_dump()
        contacts_db[normalized_name] = contact_data
        
        logger.info(f"Updated contact: {normalized_name}")
        return Contact(**contact_data)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error updating contact: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating contact '{name}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update contact: {str(e)}"
        )

@app.patch("/contacts/{name}", response_model=Contact)
async def update_contact_partial(
    name: str = Path(..., description="Contact name to update"),
    contact_update: ContactUpdate = None
):
    """
    Partially update a contact using PATCH method with path parameter.
    
    Args:
        name: Contact name (path parameter)
        contact_update: Partial contact data to update
        
    Returns:
        Updated contact
        
    Raises:
        HTTPException: If contact not found or update fails
    """
    try:
        normalized_name = normalize_name(name)
        
        # Check if contact exists
        if normalized_name not in contacts_db:
            raise HTTPException(
                status_code=404, 
                detail=f"Contact '{normalized_name}' not found"
            )
        
        # Get existing contact data
        existing_contact = contacts_db[normalized_name].copy()
        
        # Update only provided fields
        update_data = contact_update.model_dump(exclude_unset=True)
        existing_contact.update(update_data)
        
        # Store updated contact
        contacts_db[normalized_name] = existing_contact
        
        logger.info(f"Partially updated contact: {normalized_name}")
        return Contact(**existing_contact)
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error updating contact: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating contact '{name}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update contact: {str(e)}"
        )

@app.delete("/contacts/{name}")
async def delete_contact(name: str = Path(..., description="Contact name to delete")):
    """
    Delete a contact using path parameter.
    
    Args:
        name: Contact name (path parameter)
        
    Returns:
        Deletion confirmation message
        
    Raises:
        HTTPException: If contact not found or deletion fails
    """
    try:
        normalized_name = normalize_name(name)
        
        # Check if contact exists
        if normalized_name not in contacts_db:
            raise HTTPException(
                status_code=404, 
                detail=f"Contact '{normalized_name}' not found"
            )
        
        # Delete contact
        del contacts_db[normalized_name]
        
        logger.info(f"Deleted contact: {normalized_name}")
        return {
            "message": f"Contact '{normalized_name}' deleted successfully",
            "deleted_contact": normalized_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting contact '{name}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to delete contact: {str(e)}"
        )

@app.get("/contacts/stats")
async def get_contact_stats():
    """
    Get statistics about contacts in the system.
    
    Returns:
        Dictionary with contact statistics
        
    Raises:
        HTTPException: If stats cannot be calculated
    """
    try:
        total_contacts = len(contacts_db)
        
        if total_contacts == 0:
            return {
                "total_contacts": 0,
                "contact_names": [],
                "storage_type": "in-memory dictionary"
            }
        
        contact_names = list(contacts_db.keys())
        
        stats = {
            "total_contacts": total_contacts,
            "contact_names": sorted(contact_names),
            "storage_type": "in-memory dictionary"
        }
        
        logger.info(f"Generated stats for {total_contacts} contacts")
        return stats
        
    except Exception as e:
        logger.error(f"Error generating stats: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate statistics: {str(e)}"
        )

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API information and usage instructions
    """
    return {
        "message": "Contact Management System API",
        "endpoints": {
            "POST /contacts/": "Create a new contact",
            "GET /contacts/?name=John": "Get contacts with optional name filter",
            "POST /contacts/{name}": "Update a contact completely",
            "PATCH /contacts/{name}": "Update a contact partially",
            "DELETE /contacts/{name}": "Delete a contact",
            "GET /contacts/stats": "Get contact statistics"
        },
        "features": [
            "Path and query parameters",
            "In-memory dictionary storage",
            "Graceful invalid input handling",
            "Contact model: name, phone, email"
        ],
        "current_contacts": len(contacts_db)
    }