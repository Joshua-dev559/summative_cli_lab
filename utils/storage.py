import json
import os

from models.user import User
from models.project import Project
from models.task import Task

DATA_DIR = os.path.join(os.path.dirname(__file__),'..' 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _read_json(path: str):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
def _write_json(path: str, data: list):
    _ensure_data_dir()
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
        
def load_users():
    return [User.from_dict(user_data) for user_data in _read_json(USERS_FILE)]

def save_users(users: list):
    _write_json(USERS_FILE, [user.to_dict() for user in users])
    
def load_projects():
    return [Project.from_dict(project_data) for project_data in _read_json(PROJECTS_FILE)]

def save_projects(projects: list):
    _write_json(PROJECTS_FILE, [project.to_dict() for project in projects])
    
def load_tasks():
    return [Task.from_dict(task_data) for task_data in _read_json(TASKS_FILE)]

def save_tasks(tasks: list):
    _write_json(TASKS_FILE, [task.to_dict() for task in tasks])
    
def load_all():
    return {
        'users': load_users(),
        'projects': load_projects(),
        'tasks': load_tasks()
    }

    proj_map = {p.id: p for p in projects}
    for task in tasks:
        if task.project_id and task.project_id in proj_map:
            proj_map[task.project_id].add_task(task)
            
    user_map = {u.id: u for u in users}
    for project in projects:
        if project.owner_id and project.owner_id in user_map:
            user_map[project.owner_id].add_project(project)
            
    return users, projects, tasks

