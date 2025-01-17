from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    description="A simple API for managing tasks in a to-do list application",
    version="1.0.0"
)