import fastapi
from passlib.context import CryptContext
from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = fastapi.FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from routes.auth import auth_router
from routes.orders import order_router

app.include_router(auth_router)
app.include_router(order_router)

# @app.get("/")
# async def root():
#     return {"hello":"world"}
