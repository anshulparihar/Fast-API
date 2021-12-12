from pydantic import BaseModel,StrictStr,EmailStr

from blog.database import Base


class Blog(BaseModel):
    title : str
    body : str

class User(BaseModel):
    name : str
    email : EmailStr
    password : str

class ShowUser(BaseModel):
    name : str
    email : EmailStr
    class Config():
        orm_mode = True