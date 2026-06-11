import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task
from utils import storage

class TestPerson:
    def test_valid_creation(self):
        p = Person("Abel", "abel@example.com")
        assert p.name == "Abel"
        assert p.email == "abel@example.com"
        
    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            p = Person("Abel", "abel@example.com")
            p.email = "not an email"
            
    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            p = Person("Abel", "abel@example.com")
            p.name = " "
            
class TestUser:
    def test_user_inherits_person(self):
            u = User("Abel", "abel@example.com")
            assert isinstance(u, Person)
            
    def test_user_has_id(self):
            u = User("Abel", "abel@example.com")
            assert isinstance(u.id, int)
            
    def test_add_project(self):
            u = User("Abel", "abel@example.com")
            p = Project("Test", "A test project")
            u.add_project(p)
            assert len(u.projects) == 1
            
    def test_serialization_roundtrip(self):
            u = User("Abel", "abel@example.com", user_id=99)
            d = u.to_dict()
            u2 = User.from_dict(d)
            assert u.id == u2.id
            assert u.name == u2.name
            assert u.email == u2.email
            
class TestProject:
    def test_project_creation(self):
        p = Project("API Redesign", description="REST refactor", due_date="2026-05-30")
        assert p.title == "API Redesign"

    def test_empty_title_raises(self):
        p = Project("Valid Title")
        with pytest.raises(ValueError):
            p.title = ""

    def test_add_task(self):
        p = Project("Project X")
        t = Task("Write tests")
        p.add_task(t)
        assert len(p.tasks) == 1
        assert t.project_id == p.id

    def test_get_task_by_id(self):
        p = Project("Project Y")
        t = Task("Deploy", task_id=50)
        p.add_task(t)
        assert p.get_task_by_id(50)
        assert p.get_task_by_id(999) is None

    def test_serialization_roundtrip(self):
        p = Project("ML Pipeline", description="Train model", due_date="2026-06-01", owner_id=1, project_id=45)
        d = p.to_dict()
        p2 = Project.from_dict(d)
        assert p2.title == p.title
        assert p2.id == p.id
        assert p2.owner_id == p.owner_id


class TestTask:
    def test_default_status(self):
        t = Task("Fix bug")
        assert t.status == "Pending"

    def test_complete_sets_status(self):
        t = Task("Fix bug")
        t.completed()
        assert t.status == "Completed"

    def test_invalid_status_raises(self):
        t = Task("Fix bug")
        with pytest.raises(ValueError):
            t.status = "done"

    def test_serialization_roundtrip(self):
        t = Task("Write docs", assigned_to="Alice", status="In Progress", task_id=8, project_id=4)
        d = t.to_dict()
        t2 = Task.from_dict(d)
        assert t2.title == t.title
        assert t2.assigned_to == t.assigned_to
        assert t2.status == t.status
        assert t2.id == t.id
        assert t2.project_id == t.project_id


class TestStorage:
    def test_save_load_users(self, tmp_path, monkeypatch):
        monkeypatch.setattr(storage, 'USERS_FILE', str(tmp_path / 'users.json'))
        users = [User("Abel", "abel@example.com", user_id=1)]
        storage.save_users(users)
        loaded = storage.load_users()
        assert len(loaded) == 1
        assert loaded[0].name == "Abel"

    def test_save_load_projects(self, tmp_path, monkeypatch):
        monkeypatch.setattr(storage, 'PROJECTS_FILE', str(tmp_path / 'projects.json'))
        projects = [Project("Alpha", project_id=1, owner_id=1)]
        storage.save_projects(projects)
        loaded = storage.load_projects()
        assert len(loaded) == 1
        assert loaded[0].title == "Alpha"

    def test_save_load_tasks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(storage, 'TASKS_FILE', str(tmp_path / 'tasks.json'))
        tasks = [Task("Do something", task_id=1, project_id=1)]
        storage.save_tasks(tasks)
        loaded = storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0].title == "Do something"

    def test_load_missing_file_returns_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(storage, 'USERS_FILE', str(tmp_path / 'users.json'))
        assert storage.load_users() == []
            



        