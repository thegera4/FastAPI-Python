from pydantic import BaseModel


class User(BaseModel):
    id: str | None  # str for MongoDB
    username: str
    email: str
