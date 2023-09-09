from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# To start the server: uvicorn users:app --reload
# where users is the name of the file and app is the name of the FastAPI instance


class User(BaseModel):
    id: int
    username: str
    email: str
    age: int
    url: str


users_list = [User(id=1, username="thegera4", email="same@email.com", age=36, url="https://www.github.com/thegera4"),
              User(id=2, username="sarina_next", email="sarina@email.com", age=36, url="https://www.github.com/sarina"),
              User(id=3, username="asdfg", email="asdfg@email.com", age=36, url="https://www.github.com/asdfg")]


@app.get("/users")
async def users():
    return users_list


# Function to search by user id / returns the user
def search_user(user_id: int):
    selected_user = filter(lambda u: u.id == user_id, users_list)
    try:
        return list(selected_user)[0]
    except IndexError:
        return {"message": "User not found."}


# GET with Path example
@app.get("/users/{user_id}")
async def user(user_id: int):
    return search_user(user_id)


# GET with Query example
@app.get("/users/")  # Query
async def user(user_id: int):
    return search_user(user_id)


# POST example
@app.post("/users")
async def create_user(new_user: User):
    if type(search_user(new_user.id)) == User:
        # TODO:add error code
        return {"message": "User already exists."}
    else:
        users_list.append(new_user)
        return {"message": "User created successfully."}


# PUT example
@app.put("/users")
async def update_user(modified_user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == modified_user.id:
            users_list[index] = modified_user
            return {"message": "User updated successfully."}
    return {"message": "User not found."}


# DELETE example
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user_id:
            users_list.pop(index)
            return {"message": "User deleted successfully."}
    return {"message": "User not found."}
