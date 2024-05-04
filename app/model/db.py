from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DbBaseModel = declarative_base()


class Post(DbBaseModel):
    __tablename__ = "posts"

    id: Column[int] = Column(Integer, primary_key=True)
    title: Column[str] = Column(String(255), nullable=False)
    content: Column[str] = Column(String, nullable=False)
    created_at: Column[datetime] = Column(DateTime, default=lambda: datetime.now(tz=UTC))

    comments = relationship("Comment", backref="post", lazy=True)


class Comment(DbBaseModel):
    __tablename__ = "comments"

    id: Column[int] = Column(Integer, primary_key=True)
    content: Column[str] = Column(String, nullable=False)
    created_at: Column[datetime] = Column(DateTime, default=lambda: datetime.now(tz=UTC))

    post_id: Column[int] = Column(Integer, ForeignKey("posts.id"), nullable=False)
