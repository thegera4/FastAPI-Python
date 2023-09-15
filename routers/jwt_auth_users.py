from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# install: "pip install python-jose[cryptography]" to use JWT
# install: "pip install passlib[bcrypt]" to use bcrypt

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
# you can generate a random seed with "openssl rand -hex 32"
SEED = "3008f302388ba5d238ede38d2e6f8f5f19cc7151894982732755155d5e5893a3"

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "thegera4": {
        "username": "thegera4",
        "fullname": "Gerardo Medellin",
        "email": "thegera4@hotmail.com",
        "disabled": False,
        "password": "$2a$12$OKxRW5DotJfiOARAq9uF/u5GwX27gouMLeTvpVkpXIxSoZNUhenXC"
    },
    "sarina_next": {
        "username": "sarina_next",
        "fullname": "Amira Sarina",
        "email": "sarina_next@hotmail.com",
        "disabled": True,
        "password": "$2a$12$LKI2SKoCXUeTwki.KqFvNuxyTyZ0IgLYoClMG2hApuY1W6kpCeWpu"
    },
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  # ** is used to unpack the dictionary
    else:
        return 0


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])  # ** is used to unpack the dictionary
    else:
        return 0


async def authenticated_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.",
                              headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SEED, ALGORITHM).get("sub")
        if username is None:
            raise exception
        found_user = search_user(username)
        if found_user == 0:
            raise exception
        return found_user
    except JWTError:
        raise exception


async def current_user(user: User = Depends(authenticated_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user.")
    return user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form_data.username)
    if user == 0:
        raise HTTPException(status_code=400, detail="Invalid username.")

    valid_password = crypt.verify(form_data.password, user.password)
    if not valid_password:
        raise HTTPException(status_code=400, detail="Invalid password.")

    token_expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub": user.username, "exp": token_expiration}
    return {"access_token": jwt.encode(access_token, SEED, ALGORITHM), "token_type": "bearer"}


@app.get("/users/me")
async def read_me(user: User = Depends(current_user)):
    return user
