from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Satsang@123', cursor_factory= RealDictCursor)
        cursor =conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)   
        time.sleep(2) 


@app.get("/")
def root():
    return {"message": "Hello World!"}

my_posts = [{"title":"title of post 1", "content": "Content of post 1","id": 1},{"title":"favorite foods", "content": "I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
         return p
        
def find_index_post(id):
        for i,p in enumerate(my_posts):
            if p["id"] == id:
             return i

@app.get("/posts")
def root():
    return {"data": my_posts}

    
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    # print(post.model_dump())
    # return {"message": "successfully created posts"}
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail" : post}

@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    post = find_post(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found" )

    print(post)
    return {"post_detail":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    #deleteing post
    #find the index in the array that has required ID
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")

    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id : int, post: Post):
    index = find_index_post(id)

    if index == None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail = f"post with id: {id} does not exist") 

    post_dict = post.model_dump()
    post_dict["id"] = id   
    my_posts[index] = post_dict
    return {"data" : post_dict}

