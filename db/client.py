from pymongo import MongoClient
from core.config import settings

# Local
# db_client = MongoClient().local

# Remote
# Check in mongo db atlas what you need to connect in my case for python 3.11:
# python -m pip install pymongo==3.11

db_client = MongoClient(settings.mongo_uri).test  # connect to the database  "test" if it doesn't exist, create it
db_client.users.create_index("email", unique=True)  # create an index for the email field to be unique
