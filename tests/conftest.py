import pytest
from fastapi.testclient import TestClient
from taskmanager.main import app


@pytest.fixture
def client():
    return TestClient(app)
