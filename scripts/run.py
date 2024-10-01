from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routes import user_routes

app = FastAPI()

app.include_router(user_routes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI server!"}
