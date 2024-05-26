from typing import List, Optional
from fastapi import Body, FastAPI, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import crud, models, schemas
from .database import SessionLocal, engine
from .schemas import TokenData
from fastapi import Query

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not crud.verify_pass(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.post("/properties", response_model=schemas.Property)
def create_property(
    property: schemas.PropertyCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if not current_user.is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can post properties")
    return crud.create_property(db=db, property=property, user_id=current_user.id)

@app.get("/properties", response_model=List[schemas.Property])
def read_properties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    properties = crud.get_property(db, skip=skip, limit=limit)
    return properties


# Seller routes
@app.delete("/properties/{property_id}")
def delete_property(
    property_id: int = Path(..., title="The ID of the property to delete"),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    property_db = crud.get_property_by_id(db=db, property_id=property_id)
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    if property_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this property")
    return crud.delete_property(db=db, property_id=property_id)

@app.put("/properties/{property_id}")
def update_property(
    property_id: int = Path(..., title="The ID of the property to update"),
    property_details: schemas.PropertyUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    property_db = crud.get_property_by_id(db=db, property_id=property_id)
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    if property_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this property")
    updated_property = crud.update_property(db=db, property_id=property_id, property_details=property_details)
    if not updated_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated_property

# Interested in Property Route
@app.post("/properties/{property_id}/interested")
def express_interest(
    property_id: int = Path(..., title="The ID of the property of interest"),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    property_db = crud.get_property_by_id(db=db, property_id=property_id)
    if not property_db:
        raise HTTPException(status_code=404, detail="Property not found")
    seller_details = crud.get_user_by_email(db=db, email=property_db.owner.email)
    if not seller_details:
        raise HTTPException(status_code=404, detail="Seller details not found")
    return seller_details


@app.get("/properties/filter", response_model=List[schemas.Property])
def filter_properties(
    place: Optional[str] = Query(None, title="Place criteria for filtering properties"),
    area: Optional[str] = Query(None, title="Area criteria for filtering properties"),
    bedrooms: Optional[int] = Query(None, title="Bedrooms criteria for filtering properties"),
    bathrooms: Optional[int] = Query(None, title="Bathrooms criteria for filtering properties"),
    hospitalnearby: Optional[int] = Query(None, title="Hospital nearby criteria for filtering properties"),
    schoolnearby: Optional[int] = Query(None, title="School nearby criteria for filtering properties"),
    price: Optional[float] = Query(None, title="Price criteria for filtering properties"),
    db: Session = Depends(get_db)
):
    filters = schemas.FilterCriteria(
        place=place, area=area, bedrooms=bedrooms, bathrooms=bathrooms,
        hospitalnearby=hospitalnearby, schoolnearby=schoolnearby, price=price
    )
    properties = crud.filter_properties(db=db, filters=filters)
    return properties