from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "localhost",
    "http://localhost:3000",
    "localhost:3000",
    "http://192.168.92.28:3000",
    "192.168.92.28",
    "192.168.92.28:3000",
    "192.168.117.134",
    "192.168.117.134:3000",
    "http://192.168.117.134:3000",
    "http://127.0.0.1:3000",
    "127.0.0.1:3000",
    "127.0.0.1",
]

# origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

todosy = [
    {"id": "1", "item": "Read a book."},
    {"id": "2", "item": "Cycle around town."},
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


# @app.get("/todo", tags=["todos"])
# async def get_todos() -> dict:
#     return {"data": todos}


@app.get("/todo/{id}", response_model=schemas.TodoItem)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if todo:
        return todo
    else:
        print("Todo with given id not found.")
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found.")
        return


# @app.get("/todo/", tags=["todos"])
# def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     todos = crud.get_todos(db, skip=skip, limit=limit)
#     todos_json = [jsonable_encoder(todo) for todo in todos]
#     print("api.py:")
#     print(todos_json)
#     return {"data": todos_json}


@app.get("/todo/", tags=["todos"], response_model=list[schemas.TodoItem])
def get_todos(
    request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    print(request.client.host)
    todos = crud.get_todos(db, skip=skip, limit=limit)
    todos_json = [jsonable_encoder(todo) for todo in todos]
    print("api.py:")
    print(todos_json)
    return todos_json


# @app.post("/todo/", tags=["todos"])
# async def add_todo(todo: dict) -> dict:
#     todos.append(todo)
#     return {"data": {"Todo added."}}


# @app.post("/todo/", response_model=schemas.TodoItem)
# def add_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
#     if todo:
#         crud.add_todo(db, dict(todo))
#         print("api.py")
#         print(todo.dict())
#     return


@app.post("/todo/", response_model=schemas.TodoItem)
def add_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    if todo:
        return crud.add_todo(db, dict(todo))


# @app.put("/todo/{id}", response_model=schemas.TodoItem)
# def update_todo(id: int, content: str, db: Session = Depends(get_db)):
#     print(content)
#     return crud.update_todo(db, id, content)


@app.put("/todo/{id}", response_model=schemas.TodoItem)
def update_todo(id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    print(todo)
    return crud.update_todo(db, id, todo)


# @app.delete("/todo/{id}")
# def delete_todo(id: int):
#     for todo in todos:
#         if int(todo["id"]) == id:
#             todos.remove(todo)
#             return {"data": f"Todo with id {id} has been removed."}

#     return {"data": f"Todo with id {id} not found."}


@app.delete("/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, id)
