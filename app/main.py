from random import randrange
import time
from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from app.routers import posts, users, auth
from . import models, schema, utils
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

app.include_router(posts.router)
app.include_router(users.router)  
app.include_router(auth.router)        


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





