from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# To use fast Api: pip install fastapi
# To use server: pip install "uvicorn[standard]"
# To start the server: uvicorn main:app --reload
# To use mongodb: pip install pymongo

#  Routers
app.include_router(products.router)
app.include_router(users.router)

# Static files
# path is the path to expose the static files
# directory is the directory where the static files are located
# name is the name of the route
app.mount("/static", StaticFiles(directory="static"), name="static")  # http://localhost:8000/static/images/flname


@app.get("/")
async def root():
    return {"message": "This is an api made with python and fastapi."}


@app.get("/aboutMe")
async def about_me():
    return {"github": "https://www.github.com/thegera4"}
