from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import null, text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts_new"

    id = Column(Integer, primary_key=True, nullable =False)
    title = Column(String, nullable = False)
    content =  Column(String, nullable = False)
    published = Column(Boolean, server_default ='TRUE')
    created_at =  Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("now()"))
