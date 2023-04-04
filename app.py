from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
import asyncio
import motor.core

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