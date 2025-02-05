from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World!"}

my_posts = [{"title":"title of post 1", "content": "Content of post 1","id": 1},{"title":"favorite foods", "content": "I like pizza","id": 2}]


@app.get("/posts")
def root():
    return {"data": my_posts}

    
@app.post("/posts")
def create_posts(new_post: Post):
    print(new_post)
    print(new_post.model_dump())
    #return {"message": "successfully created posts"}
    return {"data": new_post}

