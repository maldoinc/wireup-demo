from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime


class PostCreateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    created_at: datetime
