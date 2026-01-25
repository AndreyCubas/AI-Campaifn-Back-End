from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class User(BaseModel):
    id: int
    email: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str
