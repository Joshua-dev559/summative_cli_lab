import argparse
import sys

from models.user import User
from models.project import Project
from models.task import Task
from utils import storage, display

def handle_add_user(args):
    users,_,_= storage.load_all()
    if any(u.email == args.email for u in users):
        display.error(f"A user with email '{args.email}'  already exists.")
        sys.exit(1)
    user = User(name=args.name, email=args.email)
    storage.save_users(users)
    display.success(f"User '{user.name}' created with ID {user.id}.")
    
def handle_list_users(args):
    users, _, _ = storage.load_all()
    display.print_users(users)
    
def handle_add_project(args):
    users, projects, _ = storage.load_all()
    owner = next((u for u in users if u.id == args.owner_id), None)
    if not owner:
        display.error(f"No user found with ID {args.user_id}.")
        sys.exit(1)
    project = Project(title=args.title, description=args.description or "",due_date=args.due_date or "", owner_id=args.user_id)
    projects.append(project)
    storage.save_projects(projects)
    display.success(f"Project '{project.title}' created with ID {project.id} for user '{owner.name}'.")
    
def handle_list_projects(args):
    users, projects, tasks = storage.load_all()
    if args.user_id:
        owner = next((u for u in users if u.id == args.user_id), None)
        if not owner:
            display.error(f"No user found with ID {args.user_id}.")
            sys.exit(1)
        filtered = [p for p in projects if p.owner_id == args.user_id]
        display.print_projects(filtered, title=f"Projects for {owner.name}")
    else:
        display.print_projects(projects)


def handle_add_task(args):
    users, projects, tasks = storage.load_all()
    project = next((p for p in projects if p.id == args.project_id), None)
    if not project:
        display.error(f"No project found with ID {args.project_id}.")
        sys.exit(1)
    task = Task(
        title=args.title,
        assigned_to=args.assigned_to or "",
        project_id=args.project_id,
    )
    tasks.append(task)
    storage.save_tasks(tasks)
    display.success(f"Task '{task.title}' created with ID {task.id} in project '{project.title}'.")


def handle_list_tasks(args):
    _, projects, tasks = storage.load_all()
    if args.project_id:
        project = next((p for p in projects if p.id == args.project_id), None)
        if not project:
            display.error(f"No project found with ID {args.project_id}.")
            sys.exit(1)
        filtered = [t for t in tasks if t.project_id == args.project_id]
        display.print_tasks(filtered, title=f"Tasks for project '{project.title}'")
    else:
        display.print_tasks(tasks)


def handle_complete_task(args):
    tasks = storage.load_tasks()
    task = next((t for t in tasks if t.id == args.task_id), None)
    if not task:
        display.error(f"No task found with ID {args.task_id}.")
        sys.exit(1)
    if task.status == "completed":
        display.error(f"Task '{task.title}' is already completed.")
        sys.exit(1)
    task.completed()
    storage.save_tasks(tasks)
    display.success(f"Task '{task.title}' marked as completed.")


def handle_update_task_status(args):
    tasks = storage.load_tasks()
    task = next((t for t in tasks if t.id == args.task_id), None)
    if not task:
        display.error(f"No task found with ID {args.task_id}.")
        sys.exit(1)
    try:
        task.status = args.status
    except ValueError as e:
        display.error(str(e))
        sys.exit(1)
    storage.save_tasks(tasks)
    display.success(f"Task '{task.title}' status updated to '{args.status}'.")


def handle_search_projects(args):
    _, projects, _ = storage.load_all()
    keyword = args.keyword.lower()
    results = [p for p in projects if keyword in p.title.lower() or keyword in p.description.lower()]
    display.print_projects(results, title=f"Search results for '{args.keyword}'")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pm",
        description="Project Management CLI — manage users, projects, and tasks.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    p_add_user = sub.add_parser("add-user", help="Create a new user.")
    p_add_user.add_argument("name", help="Full name of the user.")
    p_add_user.add_argument("email", help="Email address of the user.")
    p_add_user.set_defaults(func=handle_add_user)

    p_list_users = sub.add_parser("list-users", help="List all users.")
    p_list_users.set_defaults(func=handle_list_users)

    p_add_proj = sub.add_parser("add-project", help="Create a new project for a user.")
    p_add_proj.add_argument("user_id", type=int, help="ID of the owning user.")
    p_add_proj.add_argument("title", help="Project title.")
    p_add_proj.add_argument("--description", "-d", help="Short project description.")
    p_add_proj.add_argument("--due-date", "-D", help="Due date (2026-06-11).")
    p_add_proj.set_defaults(func=handle_add_project)

    p_list_proj = sub.add_parser("list-projects", help="List projects (optionally filter by user).")
    p_list_proj.add_argument("--user-id", "-u", type=int, help="Filter by user ID.")
    p_list_proj.set_defaults(func=handle_list_projects)

    p_add_task = sub.add_parser("add-task", help="Add a task to a project.")
    p_add_task.add_argument("project_id", type=int, help="ID of the parent project.")
    p_add_task.add_argument("title", help="Task title.")
    p_add_task.add_argument("--assigned-to", "-a", help="Name of the assignee.")
    p_add_task.set_defaults(func=handle_add_task)

    p_list_tasks = sub.add_parser("list-tasks", help="List tasks (optionally filter by project).")
    p_list_tasks.add_argument("--project-id", "-p", type=int, help="Filter by project ID.")
    p_list_tasks.set_defaults(func=handle_list_tasks)

    p_complete = sub.add_parser("completed-task", help="Mark a task as completed.")
    p_complete.add_argument("task_id", type=int, help="ID of the task to completed.")
    p_complete.set_defaults(func=handle_complete_task)

    p_update = sub.add_parser("update-task", help="Update a task's status.")
    p_update.add_argument("task_id", type=int, help="ID of the task.")
    p_update.add_argument("status", choices=["pending", "in-progress", "completed"], help="New status.")
    p_update.set_defaults(func=handle_update_task_status)

    p_search = sub.add_parser("search-projects", help="Search projects by keyword.")
    p_search.add_argument("keyword", help="Keyword to search for in title.")
    p_search.set_defaults(func=handle_search_projects)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

    
