from fastapi.testclient import TestClient
from app.main import app
from app.models import Calculation

client = TestClient(app)


def test_calculate():
    calculation = Calculation(x=2, y=4, operator="+")
    response = client.post("/calculate", json=calculation.dict())
    assert response.status_code == 200
    task_id = response.json()
    assert task_id == 1


def test_result_endpoint():
    task_id = 1
    response = client.get(f"/result/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"result": 6}


def test_task_endpoint():
    task_id = 2
    response = client.get(f"/result/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"error": "Task not found"}


def test_background_calculation():
    from app.main import perform_calculation

    calculation = Calculation(x=2, y=3, operator="+")
    result = perform_calculation(calculation)
    assert result == 5

    calculation = Calculation(x=5, y=2, operator="-")
    result = perform_calculation(calculation)
    assert result == 3

    calculation = Calculation(x=4, y=2, operator="*")
    result = perform_calculation(calculation)
    assert result == 8

    calculation = Calculation(x=10, y=2, operator="/")
    result = perform_calculation(calculation)
    assert result == 5
