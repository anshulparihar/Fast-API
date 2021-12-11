from fastapi import FastAPI
# from pydantic import BaseModel
from . import schemas,models
from .database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post('/blog')
def create(request : schemas.Blog):
    return request