from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import models, schemas


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    result = (
        db.query(models.Todo).order_by(models.Todo.id).offset(skip).limit(limit).all()
    )
    list_of_dicts = [jsonable_encoder(r) for r in result]
    print(list_of_dicts)
    return result


def add_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# def update_todo(db: Session, todo_id: int, content: str):
#     todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     print("From update_todo:")
#     print(todo_item)
#     todo_item.content = content
#     db.commit()
#     return todo_item


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    print("From update_todo:")
    print(todo_item)
    todo_item.content = todo.content
    db.commit()
    return todo_item


def delete_todo(db: Session, todo_id: int):
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_item:
        db.delete(todo_item)
        db.commit()
        db.close()
        print(f"Item with id {todo_id} deleted successfully.")
    else:
        print("Couldn't delete item. Item with given id not found")
        return
    return
