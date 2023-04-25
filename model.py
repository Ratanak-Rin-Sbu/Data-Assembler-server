from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from PyObjectId import PyObjectId
from typing import Optional
from beanie import Indexed

class User(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
  username: Indexed(str, unique=True)
  email: Indexed(EmailStr, unique=True)
  password: str
  profilePic: str
  address: str

  class Config:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    schema_extra = {
        "example": {
            "username": "Jasson Rin",
            "email": "user@example.com",
            "password": "123",
            "profilePic": "thisIsThePicturePathLink",
            "address": "TK, Phnom Penh, Cambodia"
        }
    }

  def __repr__(self) -> str:
    return f"<User {self.email}>"

  def __str__(self) -> str:
    return self.email

  def __hash__(self) -> int:
    return hash(self.email)

  def __eq__(self, other: object) -> bool:
    if isinstance(other, User):
        return self.email == other.email
    return False
  
class UpdateUserModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
  username: Optional[str]
  email: Optional[str]
  profilePic: Optional[str]
  address: Optional[str]

  class Config:
      allow_population_by_field_name = True
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
      schema_extra = {
          "example": {
              "username": "User",
              "email": "user@gmail.com",
              "profilePic": "thisIsThePicturePathLink",
              "address": "Sensok, PP, Cambodia"
          }
      }
  
class UserIn(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    email: EmailStr
    password: str

    class Config:
      allow_population_by_field_name = True
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
      schema_extra = {
          "example": {
              "email": "user@example.com",
              "password": "123",
          }
      }

class Question(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
  date: str
  query: str
  response: str
  question_type: str
  owner_id: PyObjectId = Field(default_factory=PyObjectId, alias="id")

  class Config:
      allow_population_by_field_name = True
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
      schema_extra = {
          "example": {
              "date": "3/06/2023, 8:04:23 AM",
              "query": "Number of pushups",
              "response": "40",
              "question_type": "number"
          }
      }

class UpdateQuestionModel(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
  date: Optional[str]
  query: Optional[str]
  response: Optional[str]
  question_type: Optional[str]

  class Config:
      allow_population_by_field_name = True
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
      schema_extra = {
          "example": {
              "date": "3/06/2023, 8:04:23 AM",
              "query": "Number of pushups",
              "response": "40",
              "question_type": "number"
          }
      }