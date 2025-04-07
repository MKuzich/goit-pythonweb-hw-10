from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.repository.database.db import get_db
from src.repository import contacts
from src.schemas import ContactCreate, ContactUpdate
from src.services.auth import get_current_user
from src.repository.database.models import User

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactCreate)
def create(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return contacts.create_contact(db, contact, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def read(name: str = None, email: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return contacts.get_contacts(db, current_user.id, name, email)

@router.get("/{contact_id}")
def read_one(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = contacts.get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}")
def update(contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_contact = contacts.update_contact(db, contact_id, contact_update, current_user.id)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_contact = contacts.delete_contact(db, contact_id, current_user.id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"detail": "Contact deleted"}
