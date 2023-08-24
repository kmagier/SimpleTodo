from pydantic import BaseModel
from typing import List, Dict, Union


class TodoBase(BaseModel):
    content: str


class TodoItem(TodoBase):
    id: int

    class Config:
        orm_mode = True


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


# class TodoCreate(TodoItem):
#     pass


class TodoItems(BaseModel):
    todo_items: list[TodoItem] = []

    class Config:
        orm_mode = True
