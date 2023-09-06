from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DbBaseModel = declarative_base()


class Post(DbBaseModel):
    __tablename__ = "posts"

    id: Column = Column(Integer, primary_key=True)
    title: Column = Column(String(255), nullable=False)
    content: Column = Column(String, nullable=False)
    created_at: Column = Column(DateTime, default=datetime.utcnow)

    comments = relationship("Comment", backref="post", lazy=True)


class Comment(DbBaseModel):
    __tablename__ = "comments"

    id: Column = Column(Integer, primary_key=True)
    content: Column = Column(String, nullable=False)
    created_at: Column = Column(DateTime, default=datetime.utcnow)

    post_id: Column = Column(Integer, ForeignKey("posts.id"), nullable=False)
