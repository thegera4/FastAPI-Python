from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This is an api made with python and fastapi."}


@app.get("/aboutMe")
async def about_me():
    return {"github": "https://www.github.com/thegera4"}



