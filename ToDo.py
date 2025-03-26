from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="To-Do App")

todos: Dict[int, dict] = {}
task_id_counter = 1  


class TodoItem(BaseModel):
    title: str
    description: str 
    completed: bool


@app.post("/tasks/")
def create_task(task: TodoItem):
    global task_id_counter
    task_id = task_id_counter
    todos[task_id] = task.dict()
    task_id_counter += 1
    return {"task_id": task_id, "task": todos[task_id]}


@app.get("/tasks/")
def get_tasks():
    return todos


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in todos:
        raise HTTPException(status_code=404, detail="Task not found")
    return todos[task_id]


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TodoItem):
    if task_id not in todos:
        raise HTTPException(status_code=404, detail="Task not found")
    todos[task_id] = updated_task.dict()
    return {"message": "Task updated", "task": todos[task_id]}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in todos:
        raise HTTPException(status_code=404, detail="Task not found")
    del todos[task_id]
    return {"message": "Task deleted"}

