from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datastores.database import Base, engine, get_db
from datastores.models import Driver, User
from datastores.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

app = FastAPI(
    title="Drivers API",
    description="Info about drivers"
)

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Pydantic schemas
class DriverResponse(BaseModel):
    id: int
    name: str
    age: int
    city: str
    rating: float

    class Config:
        from_attributes = True

class DriverCreate(BaseModel):
    name: str
    age: int
    city: str
    rating: float

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# Auth endpoints
@app.post("/register", status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == user.username))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    return {"message": f"User {user.username} created successfully"}


@app.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# Driver endpoints (protected)
@app.get('/drivers', response_model=list[DriverResponse])
async def get_drivers(
    city: str = None,
    limit: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Driver)

    if city:
        query = query.filter(Driver.city == city)
    if limit:
        query = query.limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@app.get('/drivers/{id}', response_model=DriverResponse)
async def fetch_driver(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Driver).filter(Driver.id == id))
    driver = result.scalars().first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@app.post('/drivers', response_model=DriverResponse, status_code=201)
async def add_driver(
    new_driver: DriverCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    driver = Driver(
        name=new_driver.name,
        age=new_driver.age,
        city=new_driver.city,
        rating=new_driver.rating
    )
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver

@app.delete("/drivers/{id}")
async def delete_driver(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Driver).filter(Driver.id == id))
    driver = result.scalars().first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    await db.delete(driver)
    await db.commit()

    return {"message": "Driver deleted"}