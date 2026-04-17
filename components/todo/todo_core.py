import json
from pathlib import Path
from datetime import datetime


TODO_FILE = Path(__file__).resolve().parents[2] / "todo.json"


class TodoCore:
    def __init__(self):
        if not TODO_FILE.exists():
            self.__todos = []

        with TODO_FILE.open("r", encoding="utf-8") as f:
            self.__todos = json.load(f)

    def __is_valid_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def __is_valid_time(self, value):
        try:
            datetime.strptime(value, "%H:%M")
            return True
        except ValueError:
            return False




    def load_tasks(self):
        if not TODO_FILE.exists():
            return []

        with TODO_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_tasks(self, tasks):
        with TODO_FILE.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)

    
    def add_task_core(self, todo_date, todo_time, todo_text):
        if not todo_date or not todo_time or not todo_text:
            return {"status": "error", "message": "Missing fields"}

        if not self.__is_valid_date(todo_date):
            return {"status": "error", "message": "Invalid date format"}

        if not self.__is_valid_time(todo_time):
            return {"status": "error", "message": "Invalid time format"}

        new_task = {
            "date": todo_date,
            "time": todo_time,
            "task": todo_text,
            "done": False,
        }

        self.__todos.append(new_task)
        self.save_tasks(self.__todos)

        return {"status": "success", "task": new_task}

    def remove_task(self, index):

        if not isinstance(index, int):
            return {"status": "error", "message": "Index must be integer"}

        if index < 0 or index >= len(self.__todos):
            return {"status": "error", "message": "Invalid index"}

        removed = self.__todos.pop(index)
        self.save_tasks(self.__todos)

        return {
            "status": "success",
            "removed": removed
        }

    def toggle_task_core(self, index):

        if not isinstance(index, int):
            return {"status": "error", "message": "Index must be integer"}

        if index < 0 or index >= len(self.__todos):
            return {"status": "error", "message": "Invalid index"}

        self.__todos[index]["done"] = not self.__todos[index].get("done", False)
        self.save_tasks(self.__todos)

        return {
            "status": "success",
            "updated": self.__todos[index]
        }
