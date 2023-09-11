from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# prefix is used to add a prefix to all the paths in the router
# tags is used to add separate "titles" to the documentation and to group the paths in the router
# responses is used to add default responses to all the paths in the router
router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "User(s) not found"}})


class User(BaseModel):
    id: int
    username: str
    email: str
    age: int
    url: str


users_list = [User(id=1, username="thegera4", email="same@email.com", age=36, url="https://www.github.com/thegera4"),
              User(id=2, username="sarina_next", email="sarina@email.com", age=36, url="https://www.github.com/sarina"),
              User(id=3, username="asdfg", email="asdfg@email.com", age=36, url="https://www.github.com/asdfg")]


@router.get("/")
async def users():
    return users_list


# Helper function to search a user by id => returns the user
def search_user(user_id: int):
    selected_user = filter(lambda u: u.id == user_id, users_list)
    try:
        return list(selected_user)[0]
    except IndexError:
        return {"message": "User not found."}


# Helper function to compare if the information is the same => raises an exception if true
def is_same_information(user1: User, user2: User):
    if (user1.username == user2.username and user1.email == user2.email and
            user1.age == user2.age and user1.url == user2.url):
        raise HTTPException(status_code=202, detail="User not modified: the received information is the same.")


# GET with Path
@router.get("/{user_id}")
async def user(user_id: int):
    return search_user(user_id)


# GET with Query
@router.get("/")
async def user(user_id: int):
    return search_user(user_id)


@router.post("/", response_model=User, status_code=201)  # response_model is for the documentation
async def create_user(new_user: User):
    if type(search_user(new_user.id)) == User:
        raise HTTPException(status_code=409, detail="User already exists.")  # raise an exception / do not return
    else:
        users_list.append(new_user)
        return new_user


@router.put("/", response_model=User, status_code=200)  # status_code is the default status code sent if OK
async def update_user(modified_user: User):
    found_user = search_user(modified_user.id)
    is_same_information(found_user, modified_user)
    for index, saved_user in enumerate(users_list):
        if saved_user.id == modified_user.id:
            users_list[index] = modified_user
            return modified_user
    raise HTTPException(status_code=404, detail="User not found.")


@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user_id:
            users_list.pop(index)
            return {"message": "User deleted successfully."}
    raise HTTPException(status_code=404, detail="User not found.")
