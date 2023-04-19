from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from PyObjectId import PyObjectId
from typing import Optional
from beanie import Indexed
from datetime import datetime

class User(BaseModel):
  id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
  username: Indexed(str, unique=True)
  email: Indexed(EmailStr, unique=True)
  password: str
  proffilePic: str
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