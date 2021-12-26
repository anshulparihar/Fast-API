from fastapi import FastAPI  
from sqlalchemy.sql.functions import mode
from . import models
from .database import engine
from .routers import blog,user

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)

app.include_router(user.router)



