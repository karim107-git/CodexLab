from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .store import load_tasks, next_task_id, save_tasks


def list_tasks(status: str | None = None, q: str | None = None) -> list[dict[str, Any]]:
    """Return task records, optionally filtered by status and search text."""
    tasks = load_tasks()
    filtered: list[dict[str, Any]] = []

    for task in tasks:
        # Fixed: compare to the actual status argument instead of the literal string "status".
        # This now properly filters tasks by the requested status.
        if status and task["status"] != status:
            continue
        # Optional case-insensitive search on title and description
        if q:
            query = q.lower()
            title = task.get("title", "").lower()
            description = task.get("description", "").lower()

            # Skip tasks that don't match the query in either field
            if query not in title and query not in description:
               continue

        # Instructor note: partial feature for the lab.
        # The route already accepts `q`, but search is not implemented yet.
        filtered.append(task)

    return filtered


def get_task(task_id: int) -> dict[str, Any] | None:
    """Find a single task by ID."""
    tasks = load_tasks()
    return next((task for task in tasks if task["id"] == task_id), None)


def create_task(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a new task and persist it."""
    tasks = load_tasks()
    task = {
        "id": next_task_id(tasks),
        "title": payload["title"],
        "description": payload["description"],
        "status": "open",
        "priority": payload["priority"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def complete_task(task_id: int) -> dict[str, Any] | None:
    """Mark a task as completed."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            #updated_task = dict(task)
            #updated_task["status"] = "done"
            #updated_task["completed_at"] = datetime.now(timezone.utc).isoformat()

            # Instructor note: intentional bug for the lab.
            # The updated task is returned, but the stored list is never updated or saved.
            #return updated_task
            # Update the task in-place so the change is reflected in the list
                 # Update the task in-place so the change is reflected in the list
            task["status"] = "done"
            task["completed_at"] = datetime.now(timezone.utc).isoformat()

           # Persist the updated tasks list to disk
            save_tasks(tasks)

            return task
            

    return None
