from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_pass_hashed(password):
    return pwd.hash(password)
def verify_pass(plain_password, hashed_password):
    return pwd.verify(plain_password,hashed_password)
def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db:Session, user: schemas.UserCreate):
    hashpass  = get_pass_hashed(user.password)
    db_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        phone=user.phone,
        hashed_password=hashpass,
        is_seller=user.is_seller
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_property(db: Session, skip:int  = 0,limit: int = 10):
    return db.query(models.Property).offset(skip).limit(limit).all()
def create_property(db: Session, property: schemas.PropertyCreate, user_id: int):
    db_property = models.Property(**property.dict(), user_id=user_id)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def get_property_by_id(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()

def delete_property(db: Session, property_id: int):
    db_property = get_property_by_id(db=db, property_id=property_id)
    if not db_property:
        return None
    db.delete(db_property)
    db.commit()
    return {"message": "Property deleted successfully"}

def update_property(db: Session, property_id: int, property_details: schemas.PropertyUpdate):
    db_property = get_property_by_id(db=db, property_id=property_id)
    if not db_property:
        return None
    for key, value in property_details.dict().items():
        setattr(db_property, key, value)
    db.commit()
    db.refresh(db_property)
    return db_property
def filter_properties(db: Session, filters: schemas.FilterCriteria):
    query = db.query(models.Property)
    if filters.place:
        query = query.filter(models.Property.place == filters.place)
    if filters.area:
        query = query.filter(models.Property.area == filters.area)
    if filters.bedrooms:
        query = query.filter(models.Property.bedrooms == filters.bedrooms)
    if filters.bathrooms:
        query = query.filter(models.Property.bathrooms == filters.bathrooms)
    if filters.hospitalnearby:
        query = query.filter(models.Property.hospitalnearby == filters.hospitalnearby)
    if filters.schoolnearby:
        query = query.filter(models.Property.schoolnearby == filters.schoolnearby)
    if filters.price:
        query = query.filter(models.Property.price == filters.price)
    return query.all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()