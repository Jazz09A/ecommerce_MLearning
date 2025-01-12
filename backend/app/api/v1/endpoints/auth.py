from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from typing import Any
from jose import JWTError, jwt
import sqlite3

from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash
from app.models.user import Token, User, UserInDB, UserCreate, UserLogin


DB_PATH = 'db/database.db'

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user(email: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT username, email, hashed_password, disabled FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    print(f"Query result for email '{email}': {row}")

    connection.close()

    if row is None:
        return None

    user_dict = {
        "username": row[0],
        "email": row[1],
        "hashed_password": row[2],
        "disabled": row[3]
    }

    return UserInDB(**user_dict)

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"Token payload: {payload}")
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        print(f"User email from token: {email}")

    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    user = get_user(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(user_credentials: UserLogin) -> Any:
    user = authenticate_user(user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username or password incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    return current_user 


@router.post("/register", response_model=User)
def register_user(user_credentials: UserCreate):
    print(f"Received registration request: {user_credentials}")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Check if the email already exists
    cursor.execute('SELECT email FROM users WHERE email = ?', (user_credentials.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        connection.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user_credentials.password)

    cursor.execute('''
    INSERT INTO users (username, email, hashed_password)
    VALUES (?, ?, ?)
    ''', (user_credentials.username, user_credentials.email, hashed_password))

    connection.commit()
    connection.close()

    # Return the created user object
    return User(username=user_credentials.username, email=user_credentials.email)


@router.get("/users")
def get_users():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()