from pydantic import BaseModel,StrictStr,EmailStr
from typing import List, Optional
from blog.database import Base


class Blog(BaseModel):
    title : str
    body : str
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    name : str
    email : EmailStr
    blogs:List[Blog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    
    title : str
    body : str
    creator : ShowUser
    class Config():
        orm_mode = True
        
class User(BaseModel):
    name : str
    email : EmailStr
    password : str

class Login(BaseModel):
    username:str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None