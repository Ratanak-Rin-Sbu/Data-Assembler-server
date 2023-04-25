from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from model import User, UserIn, Question, UpdateQuestionModel
from typing import Optional
from auth.config import settings
from auth.security import get_password, verify_password, create_access_token
from PyObjectId import PyObjectId

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
# Question DB
questionDB = client.QuestionList
questionCollection = questionDB.question

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

# QUESTION
# GET ONE QUESTION
async def fetch_one_question(id, userId):
    document = await questionCollection.find_one({"id": id, "owner_id": userId})
    return document

@app.get("/api/{userId}/question/{id}", response_model=Question)
async def get_question_by_id(id: PyObjectId, userId: PyObjectId):
    response = await fetch_one_question(id, userId)
    if response:
        return response
    raise HTTPException(404, f"There is no question with the id {id}")

# GET ALL questions
async def fetch_all_questions(userId):
    questions = []
    cursor = questionCollection.find({})
    async for document in cursor:
        if document["owner_id"] == userId:
            questions.append(Question(**document))
    return questions

@app.get("/api/{userId}/questions")
async def get_questions(userId: PyObjectId):
    response = await fetch_all_questions(userId)
    return response

# CREATE A Question
async def create_question(question, userId):
    document = question
    document["owner_id"] = userId
    result = await questionCollection.insert_one(document)
    return document

@app.post("/api/{userId}/question", response_model=Question)
async def post_qustion(question: Question, userId: PyObjectId):
    cursor = questionCollection.find({})
    async for document in cursor:
        if document["owner_id"] == userId:
            response = await create_question(question.dict(), userId)
            if response:
                return response
            raise HTTPException(400, "Something went wrong")
    raise HTTPException(404, f"There is no user with the id {userId}")
    
    # response = await create_question(question.dict(), userId)
    # if response:
    #     return response
    # raise HTTPException(400, "Something went wrong")

# UPDATE A QUESTION
async def update_question(id: PyObjectId, question: UpdateQuestionModel, userId: PyObjectId):
    if question.date != None:
        await questionCollection.update_one({"id": id}, {"$set": {"date": question.date}})
    if question.query != None:
        await questionCollection.update_one({"id": id}, {"$set": {"query": question.query}})
    if question.response != None:
        await questionCollection.update_one({"id": id}, {"$set": {"response": question.response}})
    if question.question_type != None:
        await questionCollection.update_one({"id": id}, {"$set": {"question_type": question.question_type}})
    document = await questionCollection.find_one({"id": id, "owner_id": userId})
    return document

@app.put("/api/{userId}/question/{id}", response_model=Question)
async def put_question(id: PyObjectId, question: UpdateQuestionModel, userId: PyObjectId):
    response = await update_question(id, question, userId)
    if response:
        return response
    raise HTTPException(404, f"There is no question with the id {id}")

# DELETE A QUESTION
async def remove_question(id: PyObjectId, userId: PyObjectId):
    await questionCollection.delete_one({"id": id, "owner_id": userId})
    return True

@app.delete("/api/{userId}/question/{id}")
async def delete_question(id: PyObjectId, userId: PyObjectId):
    response = await remove_question(id, userId)
    if response:
        return "Successfully deleted question"
    raise HTTPException(404, f"There is no question with the id {id}")