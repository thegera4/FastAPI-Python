from pymongo import MongoClient

# Local
# db_client = MongoClient().local

# Remote
# Check in mongo db atlas what you need to connect in my case for python 3.11:
# python -m pip install pymongo==3.11
DB_URL = 'mongodb+srv://thegera:NNrGyIvljGzbss2h@cluster0.reu5biw.mongodb.net/?retryWrites=true&w=majority'
db_client = MongoClient(DB_URL).test  # test is the name of the database that will be created if it doesn't exist
db_client.users.create_index("email", unique=True)  # create an index for the email field to be unique
