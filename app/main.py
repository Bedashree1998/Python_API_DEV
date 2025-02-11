from random import randrange
import time
from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema
from sqlalchemy.orm import Session
from .database import engine,get_db

models.Base.metadata.create_all(bind = engine)

app = FastAPI()
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

# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#     return {"status" : "success"}
    

my_posts = [{"title":"title of post 1", "content": "Content of post 1","id": 1},{"title":"favorite foods", "content": "I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
         return p
        
def find_index_post(id):
        for i,p in enumerate(my_posts):
            if p["id"] == id:
             return i

@app.get("/posts", response_model=List[schema.Post])
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    print(type(db))

    posts = db.query(models.Post).all()
    return {"data": posts}

    
@app.post("/posts", status_code= status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post: schema.PostCreate ,db:Session = Depends(get_db)):
    # print(post)
    # print(post.model_dump())
    # return {"message": "successfully created posts"}

    #Before connecting to the database
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0,100000)
    # my_posts.append(post_dict)

    #after connection to the database
    # cursor.execute(f"INSERT INTO posts(title, content,published) VALUES({post.title},{post.content})") --- this is vulnerable to SQL injection so its not preferred
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #using SQLAlchemy
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(post.model_dump)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail" : post}

@app.get("/posts/{id}", response_model=schema.Post)
def get_post(id : int,db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found" )

    return {"post_detail":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session = Depends(get_db)):
    #deleteing post
    #find the index in the array that has required ID
    # index = find_index_post(id)

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    
    post.delete(synchronise_session = False)
    db.commit()

    
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schema.Post)
def update_post(id : int, updated_post: schema.PostCreate, db:Session = Depends(get_db)):
    # index = find_index_post(id)
    #steps for SQl Query
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, Published = %s WHERE id = %s RETURNING * """
    #                ,(post.title, post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    detail = f"post with id: {id} does not exist") 

    # post_dict = post.model_dump()
    # post_dict["id"] = id   
    # my_posts[index] = post_dict

    post_query.update(update_post.model_dump(),synchronise_session = False)
    db.commit()
    return {"data" : post_query.first()}

