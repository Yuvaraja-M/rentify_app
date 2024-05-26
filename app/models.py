from sqlalchemy import Column, String,Integer, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    hashed_password = Column(String)
    is_seller = Column(Boolean, default=False)

    properties = relationship("Property",back_populates="owner")

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    user_id =  Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    place = Column(String)
    area = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    hospitalnearby = Column(Integer)
    schoolnearby = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    owner = relationship("User", back_populates="properties")