# Task Manager API

A simple FastAPI-based Task Manager API for managing to-do list tasks.

## Features

- Create, read, update, and delete tasks
- Filter tasks by completion status
- Automatic OpenAPI documentation
- Full test coverage
- Poetry dependency management

## Setup

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Run the application:
```bash
poetry run uvicorn taskmanager.main:app --reload
```

4. Access the API documentation:
   - OpenAPI UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Running Tests

```bash
poetry run pytest
```

coverage report:

```bash
poetry run pytest --cov=taskmanager --cov-report=term-missing --cov-report=html
```

### Type Checking

Run Pyright type checking:
```bash
poetry run pyright
```

### Formatting

```bash 
poetry run black taskmanager tests
```
