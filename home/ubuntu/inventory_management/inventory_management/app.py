from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from datetime import datetime, timedelta
import jwt
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Secret key for JWT token
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class User(BaseModel):
    username: str
    email: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Client(BaseModel):
    id: int
    name: str
    contact_email: str
    contact_phone: str

class License(BaseModel):
    id: str
    user_id: int
    expiration_date: datetime
    features: List[str]

# Mock database (replace with actual database in production)
users_db = {
    "testuser": {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": get_password_hash("password123")
    },
    "newuser": {
        "username": "newuser",
        "email": "newuser@example.com",
        "hashed_password": get_password_hash("newpassword")
    }
}
clients_db = {}
licenses_db = {}

# Print stored hashed password for "newuser"
print(f"Stored hashed password for newuser: {users_db['newuser']['hashed_password']}")

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/clients/", response_model=Client)
async def create_client(client: Client, current_user: User = Depends(get_current_user)):
    clients_db[client.id] = client.dict()
    return client

@app.get("/api/clients/", response_model=List[Client])
async def read_clients(current_user: User = Depends(get_current_user)):
    return list(clients_db.values())

@app.post("/licenses/", response_model=License)
async def create_license(user_id: int, features: List[str], current_user: User = Depends(get_current_user)):
    license_id = str(uuid.uuid4())
    expiration_date = datetime.utcnow() + timedelta(days=365)  # 1 year license
    new_license = License(id=license_id, user_id=user_id, expiration_date=expiration_date, features=features)
    licenses_db[license_id] = new_license.dict()
    return new_license

@app.get("/licenses/{license_id}", response_model=License)
async def read_license(license_id: str, current_user: User = Depends(get_current_user)):
    if license_id not in licenses_db:
        raise HTTPException(status_code=404, detail="License not found")
    return licenses_db[license_id]

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
