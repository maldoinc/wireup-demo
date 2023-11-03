from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostGetModel(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime


class PostCreateModel(BaseModel):
    title: str
    content: str
    created_at: datetime
