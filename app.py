from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from model import User, UserIn
from typing import Optional
from auth.config import settings
from auth.security import get_password, verify_password, create_access_token

# DB
import motor.motor_asyncio
import asyncio
import motor.core

# Auth
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(
    title="DataAssembler",
)

# DATABASE SETUP
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://jassonrin:stfuimissHER0730@cluster0.z587qgx.mongodb.net/?retryWrites=true&w=majority')
client.get_io_loop = asyncio.get_running_loop
# User DB
userDB = client.UserList
userCollection = userDB.user

# CORS SETUP
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
@app.get("/")
def read_root():
	return {"data":"Hello World"}

# AUTH
# TOKEN
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl = "/login",
    scheme_name = "JWT"
)

# REGISTER USER
async def create_user(user):
    document = user
    result = await userCollection.insert_one(document)
    return document

@app.post("/user", response_model=User)
async def post_user(user: User):
    existed_username = await userCollection.find_one({'username': {'$eq': user.username}})
    existed_email = await userCollection.find_one({'email': {'$eq': user.email}})
    if existed_username or existed_email:
        raise HTTPException(403, "Username or email already exists")
    else:
        user = user.dict()
        user["password"] = get_password(user["password"])
        response = await create_user(user)
        if response:
            return response
        else:
            raise HTTPException(400, "Something went wrong")
        

# LOGIN
async def authenticate(email: str, password: str) -> Optional[User]:
    user = await userCollection.find_one({'email': {'$eq': email}})
    if not user:
        return None
    if not verify_password(password=password, hashed_pass=user["password"]):
        return None
    return user

@app.post("/login", summary="Create token for user")
async def login(user: UserIn):
    user = await authenticate(user.email, user.password)
    if not user:
        raise HTTPException(400, "Incorrect email or password")
    return {
        "access_token": create_access_token(user["id"]),
        "user": {
            "_id": str(user["_id"]),
            "id": str(user["id"]),
            "username": user["username"],
            "email": user["email"],
            "password": user["password"],
            "profilePic": user["profilePic"],
            "address": user["address"]
        },
    }