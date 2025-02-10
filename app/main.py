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
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

    
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    # print(post.model_dump())
    # return {"message": "successfully created posts"}

    #Before connecting to the database
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0,100000)
    # my_posts.append(post_dict)

    #after connection to the database
    # cursor.execute(f"INSERT INTO posts(title, content,published) VALUES({post.title},{post.content})") --- this is vulnerable to SQL injection so its not preferred
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail" : post}

@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found" )

    return {"post_detail":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    #deleteing post
    #find the index in the array that has required ID
    # index = find_index_post(id)

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()



    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")

    
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id : int, post: Post):
    # index = find_index_post(id)

    cursor.execute("""UPDATE posts SET title = %s, content = %s, Published = %s WHERE id = %s RETURNING * """
                   ,(post.title, post.content,post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail = f"post with id: {id} does not exist") 

    # post_dict = post.model_dump()
    # post_dict["id"] = id   
    # my_posts[index] = post_dict
    return {"data" : updated_post}

