from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None  # Optional and str for mongo
    username: str
    email: str
