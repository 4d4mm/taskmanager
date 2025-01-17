from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from taskmanager.models import TaskParameters, TaskOptionalParameters, TaskInDB
from taskmanager.schema import Task
from taskmanager.database import SessionLocal, engine, Base

app = FastAPI(
    title="Task Manager API", description="A simple API for managing tasks in a to-do list application", version="1.0.0"
)

# Create the database tables, this is an oversimplified initialisation
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=TaskInDB, status_code=201)
async def create_task(task: TaskParameters, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=list[TaskInDB])
async def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    db: Session = Depends(get_db),
):
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    return query.all()


@app.get("/tasks/{task_id}", response_model=TaskInDB)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskInDB)
async def update_task(task_id: int, task: TaskParameters, db: Session = Depends(get_db)):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=False).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@app.patch("/tasks/{task_id}", response_model=TaskInDB)
async def partially_update_task(task_id: int, task: TaskOptionalParameters, db: Session = Depends(get_db)):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
