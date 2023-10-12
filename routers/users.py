from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId  # to convert the id from mongo to a string
from pymongo.errors import DuplicateKeyError

# prefix is used to add a prefix to all the paths in the router
# tags is used to add separate "titles" to the documentation and to group the paths in the router
# responses is used to add default responses to all the paths in the router
router = APIRouter(
    prefix="/users", tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"description": "User(s) not found"}}
)


# Auxiliary function to search a user in the database by a certain field/key => returns the user (model)
def search_user(field: str, key):
    found_user = db_client.users.find_one({field: key})
    print(found_user)
    if found_user is None:
        raise None
    return user_schema(found_user)
    #try:
        #found_user = user_schema(db_client.users.find_one({field: key}))
        #return User(**found_user)
    #except IndexError:
        #return {"message": "User not found."}


# Auxiliary function to compare if the information of 2 Users is the same => raises an exception if true
def is_same_information(user1: User, user2: User):
    if (user1.username == user2.username and user1.email == user2.email and
            user1.age == user2.age and user1.url == user2.url):
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="User NOT modified, information is the same.")


@router.get("/", response_model=list[User])  # response_model is for the documentation
async def users():
    return users_schema(db_client.users.find())


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
    try:
        new_user_dict = dict(new_user)  # convert the model to a dict
        del new_user_dict["id"]  # delete the id field because mongo will create it automatically
        user_id = db_client.users.insert_one(new_user_dict).inserted_id  # insert the user and get the id
        transformed_user = user_schema(db_client.users.find_one({"_id": user_id}))  # get the user by id
        return User(**transformed_user)  # return the user as a model
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with the same email already exists.")


@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(modified_user: User):
    # found_user = search_user(modified_user.id)
    # is_same_information(found_user, modified_user)
    modified_user_dict = dict(modified_user)
    del modified_user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(modified_user.id)}, modified_user_dict)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return search_user("_id", ObjectId(modified_user.id))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    found_user = db_client.users.find_one_and_delete({"_id": ObjectId(user_id)})
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
