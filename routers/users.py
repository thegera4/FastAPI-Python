from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from db.utils.aux_defs import search_user  # , is_same_information
from bson import ObjectId  # to convert the id from mongo to a string

# prefix is used to add a prefix to all the paths in the router
# tags is used to add separate "titles" to the documentation and to group the paths in the router
# responses is used to add default responses to all the paths in the router
router = APIRouter(
    prefix="/users", tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"description": "User(s) not found"}}
)


@router.get("/", response_model=list[User])  # response_model is for the documentation
async def users():
    return users_schema(db_client.local.users.find())


# GET with Path
@router.get("/{user_id}")
async def user(user_id: str):
    return search_user("_id", ObjectId(user_id))


# GET with Query
@router.get("/")
async def user(user_id: str):
    return search_user("_id", ObjectId(user_id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)  # status_code = default code if OK
async def create_user(new_user: User):
    # if user is found in the database, raise an exception
    if type(search_user("email", new_user.email)) == User:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    # else, create the user
    new_user_dict = dict(new_user)  # convert the model to a dict
    del new_user_dict["id"]  # delete the id from the dict to insert into mongo
    user_id = db_client.local.users.insert_one(new_user_dict).inserted_id  # insert the user into mongo and take the id
    transformed_user = user_schema(db_client.local.users.find_one({"_id": user_id}))  # transform the user to a model
    return User(**transformed_user)  # ** to unpack the dict


@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(modified_user: User):
    # found_user = search_user(modified_user.id)
    # is_same_information(found_user, modified_user)
    modified_user_dict = dict(modified_user)
    del modified_user_dict["id"]
    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(modified_user.id)}, modified_user_dict)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return search_user("_id", ObjectId(modified_user.id))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    found_user = db_client.local.users.find_one_and_delete({"_id": ObjectId(user_id)})
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
