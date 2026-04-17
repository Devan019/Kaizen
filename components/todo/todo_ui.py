from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import ttk
import customtkinter as ctk
from pathlib import Path
import os
from .todo_core import TodoCore
TODO_FILE = Path(__file__).resolve().parents[2] / "todo.json"

class TodoUI:

    def __init__(self):
        self.tc = TodoCore()
        self.tasks = []

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.app = ctk.CTk()
        self.app.title("Todo Manager")
        self.app.geometry("980x600")

        self.setup_ui()
        self.load_and_refresh()

        self.last_modified = 0
        self.watch_file()

    # ================= UI SETUP =================
    def setup_ui(self):
        self.table_frame = ctk.CTkFrame(self.app)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1f1f1f",
            foreground="#f0f0f0",
            fieldbackground="#1f1f1f",
            rowheight=34,
            font=("Segoe UI", 14),
        )

        style.configure(
            "Treeview.Heading",
            background="#2b2b2b",
            foreground="#ffffff",
            font=("Segoe UI", 15, "bold"),
        )

        style.map("Treeview", background=[("selected", "#264f78")])

        columns = ("date", "time", "task", "done")

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=14
        )

        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("task", text="Todo")
        self.tree.heading("done", text="Status")

        self.tree.column("date", width=140, anchor="center")
        self.tree.column("time", width=120, anchor="center")
        self.tree.column("task", width=530, anchor="w")
        self.tree.column("done", width=130, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ================= DATA =================
    def load_and_refresh(self):
        self.tasks = self.tc.load_tasks()
        self.refresh_table()

    # ================= TABLE =================
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, task_item in enumerate(self.tasks):
            status = "Done" if task_item.get("done", False) else "Pending"

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    task_item.get("date", ""),
                    task_item.get("time", ""),
                    task_item.get("task", ""),
                    status,
                ),
            )

    def watch_file(self):
        try:
            current_mtime = os.path.getmtime(TODO_FILE)

            if current_mtime != self.last_modified:
                print("File changed!")   # debug

                self.last_modified = current_mtime

                new_tasks = self.tc.load_tasks()

                if new_tasks != self.tasks:
                    self.tasks = new_tasks
                    self.refresh_table()

        except Exception as e:
            print("Watcher error:", e)

        self.app.after(500, self.watch_file)

    # ================= RUN =================
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    last_modified = 0
    ui = TodoUI()
    ui.run()
