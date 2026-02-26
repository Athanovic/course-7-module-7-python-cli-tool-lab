import sys
import io

# Fix Windows emoji output
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import argparse
from lib.models import Task, User

# In-memory storage
users = {}


def add_task(args):
    if args.user not in users:
        users[args.user] = User(args.user)

    user = users[args.user]

    task = Task(args.title)
    user.add_task(task)


def complete_task(args):
    user = users.get(args.user)

    if not user:
        print("User not found.")
        return

    task = user.get_task(args.title)

    if not task:
        print("Task not found.")
        return

    task.complete()


def list_tasks(args):
    user = users.get(args.user)

    if not user:
        print("User not found.")
        return

    if not user.tasks:
        print("No tasks found.")
        return

    for task in user.tasks:
        status = "✓" if task.completed else "✗"
        print(f"[{status}] {task.title}")


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Add Task
    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    # Complete Task
    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    # List Tasks
    list_parser = subparsers.add_parser("list", help="List tasks for a user")
    list_parser.add_argument("user")
    list_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()