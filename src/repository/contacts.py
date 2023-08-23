from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactsSchema, ContactsUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    sq = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    sq = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contacts_id: int, db: AsyncSession, user: User):
    sq = select(Contact).filter_by(id=contacts_id, user=user)
    contact = await db.execute(sq)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactsSchema, db: AsyncSession, user: User):
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, bd=body.bd, city=body.city, notes=body.notes, user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(todo_id: int, body: ContactsUpdateSchema, db: AsyncSession, user: User):
    sq = select(Contact).filter_by(id=todo_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.bd = body.bd
        contact.city = body.city
        contact.notes = body.notes
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession, user: User):
    sq = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact