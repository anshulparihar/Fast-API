from fastapi import FastAPI
from typing import Optional, Text
from pydantic import BaseModel
app = FastAPI()

@app.get('/blog')   #app is a variable name act as FastAPI instance
def index(limit = 10, published :bool = True, sort: Optional[str] = None):
    return {'data':'blog list'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'Unpublished Blogs'}


@app.get('/blog/{id}')
def show(id:int):
    return{'data':id}


class Blog(BaseModel):      #Creating a base model for the blog
    title : str
    body : str
    published_at : Optional[bool]



@app.get('/blog/{id}/comment')
def comment(id):
    return {'data' :{'1','2'} }

#We are using Post request while creating the new blog
@app.post('/blog')
def create_blog(request: Blog):     #Using the base model
    #return request
    return {'data':f'blog is created {request}'}
