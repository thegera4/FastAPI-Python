import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

# pip install python-dotenv
# pip install pydantic-settings

# Load the environment variables from the .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# Class to configure FastAPI so we can use environment variables
class Settings(BaseSettings):
    api_name: str = "FastAPI-Python-MongoDB"
    admin_email: str = "thegera4@hotmail.com"
    items_per_user: int = 50
    api_version: str = "1.0.0"
    mongo_uri: str = os.getenv("MONGO_URI")

    class Config:
        env_file = ".env"


# Create an instance of the settings class
settings = Settings()
