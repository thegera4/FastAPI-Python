from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# To start the server: uvicorn users:app --reload
# where users is the name of the file and app is the name of the FastAPI instance


class User(BaseModel):
    username: str
    email: str
    age: int
    url: str


users_list = [User(username="thegera4", email="same@email.com", age=36, url="https://www.github.com/thegera4"),
              User(username="sarina_next", email="sarina@email.com", age=36, url="https://www.github.com/sarina"),
              User(username="asdfg", email="asdfg@email.com", age=36, url="https://www.github.com/asdfg")]


@app.get("/users")
async def users():
    return users_list
