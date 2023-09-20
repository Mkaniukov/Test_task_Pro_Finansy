from fastapi import FastAPI, BackgroundTasks
from typing import List

from app.models import Task, Calculation

app = FastAPI()

tasks = {}


def perform_calculation(calculation: Calculation) -> int | float | str:
    x = calculation.x
    y = calculation.y
    operator = calculation.operator

    if operator == "+":
        return x + y
    elif operator == "-":
        return x - y
    elif operator == "*":
        return x * y
    elif operator == "/":
        try:
            return x / y
        except ZeroDivisionError:
            return "Error: Cannot divide by zero"


@app.post("/calculate")
async def calculate(
        calculation: Calculation, background_tasks: BackgroundTasks
) -> int:
    task_id = len(tasks) + 1

    def perform_background_calculation():
        result = perform_calculation(calculation)
        tasks[task_id]["result"] = result
        tasks[task_id]["status"] = "completed"

    tasks[task_id] = {"status": "in progress"}
    background_tasks.add_task(perform_background_calculation)

    return task_id


@app.get("/result/{task_id}")
async def get_result(task_id: int):
    if task_id not in tasks:
        return {"error": "Task not found"}

    if "result" not in tasks[task_id]:
        return {"status": tasks[task_id]["status"]}

    return {"result": tasks[task_id]["result"]}


@app.get("/tasks")
async def get_tasks() -> List[Task]:
    task_list = []
    for task_id, task_data in tasks.items():
        task_list.append(Task(id=task_id, status=task_data["status"]))
    return task_list
