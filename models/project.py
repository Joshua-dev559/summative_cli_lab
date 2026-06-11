from models.task import Task

class Project:
    
    _id_counter = 1
    
    def __init__(self, title: str, description: str = "", due_date: str = None, owner_id: int = None, project_id: int = None):
        if project_id is not None:
            self.id = project_id
            Project._id_counter = max(Project._id_counter, project_id + 1)
        else:
            self.id = Project._id_counter
            Project._id_counter += 1
            
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.tasks = []
        
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
        
    def add_task(self, task: Task):
        task.project_id = self.id
        self.tasks.append(task)
        
    def get_task_by_id(self, task_id: int):
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'owner_id': self.owner_id,
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data['title'],
            description=data.get('description', ''),
            due_date=data.get('due_date', ''),
            owner_id=data.get('owner_id'),
            project_id=data['id']
        )
        
    def __str__(self):
        due = f" - Due: {self.due_date}" if self.due_date else ""
        return f"[{self.id}] {self.title}{due} - Tasks: {len(self.tasks)}"
        