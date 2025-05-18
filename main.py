"""
TODO: add, update, delete tasks
mark a task as in progress or done
list all tasks, tasks that are done/not done/inprogress
"""
import argparse
import json
import os
from enum import Enum
import time
import logging
logging.basicConfig(level=logging.DEBUG)

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
        
def get_parser():
    parser = argparse.ArgumentParser("Todo notes")
    parser.add_argument("--version", "-V", action="store_true", help="Show version")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose mode"
    )
    subparsers = parser.add_subparsers(title="Commands", dest="cmd")
    
    add = subparsers.add_parser("add", help="Add new task")
    add.add_argument("title", help="Todo title")
    add.add_argument("--description", help="Task description")
    add.add_argument("--status", choices=[s.value for s in TaskStatus], default=TaskStatus.TODO.value, help="Task status")
    
    show = subparsers.add_parser("show", help="Show tasks")
    show.add_argument("--all", action="store_true", help="Show all the tasks")
    show.add_argument("--todo", action="store_true", help="Show only TODO tasks")
    show.add_argument("--in-progress", action="store_true", help="Show only IN PROGRESS tasks")
    show.add_argument("--done", action="store_true", help="Show only DONE tasks")
    
    update = subparsers.add_parser("update", help="Update tasks")
    update.add_argument("number", type=int, help="Task number")
    update.add_argument("--title", help="New title for the task")
    update.add_argument("--description", help="New description for the task")
    update.add_argument("--status", choices=[s.value for s in TaskStatus], 
                       help="New status for the task")
    
    done = subparsers.add_parser("done", help="Mark task as done")
    done.add_argument("number", type=int, help="Task number")
    
    remove = subparsers.add_parser("remove", help="Remove task")
    remove.add_argument("number", type=int, help="Task number")
    
    return parser

def add_task(args):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": args.title,
        "description": args.description or "",
        "status": args.status,
        "createdAt": time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()),
        "updatedAt": None
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task #{new_task['id']}: {args.title}")

def show_tasks(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    if args.all or not (args.todo or args.in_progress or args.done):
        filtered_tasks = tasks
    else:
        status_filters = []
        if args.todo:
            status_filters.append(TaskStatus.TODO.value)  # "todo"
        if args.in_progress:
            status_filters.append(TaskStatus.IN_PROGRESS.value)  # "in_progress"
        if args.done:
            status_filters.append(TaskStatus.DONE.value)  # "done"
    
        filtered_tasks = [t for t in tasks if t["status"] in status_filters]
        
    if not filtered_tasks:
        print("No tasks match the specified filters.")
        return
    
    for task in filtered_tasks:
        print(f"#{task['id']} [{task['status'].upper()}] {task['title']}")
        print(f"Created: {task['createdAt']}")
        if args.verbose and task['description']:
            print(f"{task['description']}")
            if task["updatedAt"]:
                print(f"Updated: {task['updatedAt']}")


            
def update_task(args):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == args.number), None)
    
    if not task:
        print(f"Task #{args.number} not found.")
        return
    
    if args.title:
        task["title"] = args.title
    if args.description:
        task["description"] = args.description
    if args.status:
        task["status"] = args.status
    task.update({"updatedAt": time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())})
    save_tasks(tasks)
    print(f"Updated task #{args.number}")
    
def mark_done(args):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == args.number), None)
    if not task:
        print(f"Task #{args.number} not found.")
        return
    task["status"] = TaskStatus.DONE.value
    save_tasks(tasks)
    print(f"Marked task #{args.number} as done")
    
def remove_task(args):
    tasks = load_tasks()
    task_index = next((i for i, t in enumerate(tasks) if t["id"] == args.number), None)
    
    if task_index is None:
        print(f"Task #{args.number} not found.")
        return
    
    removed_task = tasks.pop(task_index)
    save_tasks(tasks)
    print(f"Removed task #{args.number}: {removed_task['title']}")

def main():
    parser = get_parser()
    args = parser.parse_args()
    
    if args.version:
        print("TODO App v1.0")
        return
    
    if not hasattr(args, "cmd"):
        parser.print_help()
        return
    
    try:
        if args.cmd == "add":
            add_task(args)
        elif args.cmd == "show":
            show_tasks(args)
        elif args.cmd == "remove":
            remove_task(args)
        elif args.cmd == "update":
            update_task(args)
        elif args.cmd == "done":
            mark_done(args)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()