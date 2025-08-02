# main.py
from fastapi import FastAPI, HTTPException, Query
from models import ContactCreate, Contact
from file_handler import read_contacts, write_contacts
import re

app = FastAPI()

def generate_id(contact: ContactCreate) -> str:
    return re.sub(r'[^\w\-]', '_', contact.name.lower())

@app.post("/contacts", status_code=201)
async def create_contact(contact: ContactCreate):
    try:
        contacts = read_contacts()
        contact_id = generate_id(contact)
        if contact_id in contacts:
            raise HTTPException(status_code=400, detail="Contact with this name already exists")
        contact_data = Contact(**contact.model_dump(), id=contact_id)
        contacts[contact_id] = contact_data.model_dump()
        write_contacts(contacts)
        return contact_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create contact: {str(e)}")

@app.get("/contacts")
async def get_contacts(name: str = Query(None)):
    try:
        contacts = read_contacts()
        if not name:
            return [Contact(**data) for data in contacts.values()]
        return [
            Contact(**data)
            for data in contacts.values()
            if data['name'].lower() == name.lower()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve contacts: {str(e)}")

@app.put("/contacts/{name}")
async def update_contact(name: str, contact: ContactCreate):
    try:
        contacts = read_contacts()
        contact_id = re.sub(r'[^\w\-]', '_', name.lower())
        if contact_id != generate_id(contact):
            raise HTTPException(status_code=400, detail="Name in URL must match contact name")
        if contact_id not in contacts:
            raise HTTPException(status_code=404, detail="Contact not found")
        contact_data = Contact(**contact.model_dump(), id=contact_id)
        contacts[contact_id] = contact_data.model_dump()
        write_contacts(contacts)
        return contact_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update contact: {str(e)}")

@app.delete("/contacts/{name}")
async def delete_contact(name: str):
    try:
        contacts = read_contacts()
        contact_id = re.sub(r'[^\w\-]', '_', name.lower())
        if contact_id not in contacts:
            raise HTTPException(status_code=404, detail="Contact not found")
        del contacts[contact_id]
        write_contacts(contacts)
        return {"detail": f"Contact {name} deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete contact: {str(e)}")