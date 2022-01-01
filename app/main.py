from fastapi import FastAPI  
from sqlalchemy.sql.functions import mode

from blog.routers import authentication
from blog import models
from blog.database import engine
from blog.routers import blog,user,authentication

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)

app.include_router(blog.router)

app.include_router(user.router)



