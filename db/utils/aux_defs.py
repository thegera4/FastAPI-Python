from db.models.user import User
from fastapi import HTTPException, status
from db.schemas.user import user_schema
from db.client import db_client


# Auxiliary function to search a user in the database by a certain field/key => returns the user (model)
def search_user(field: str, key):
    try:
        found_user = user_schema(db_client.local.users.find_one({field: key}))
        return User(**found_user)
    except IndexError:
        return {"message": "User not found."}


# Auxiliary function to compare if the information of 2 Users is the same => raises an exception if true
def is_same_information(user1: User, user2: User):
    if (user1.username == user2.username and user1.email == user2.email and
            user1.age == user2.age and user1.url == user2.url):
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="User NOT modified, information is the same.")
