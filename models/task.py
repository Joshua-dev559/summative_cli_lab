VALID_STATUSES = ["Pending", "In Progress", "Completed"]

class Task:
    
    _id_counter = 1
    
    def __init__(self, title: str, description: str, assigned_to: str = "", status: str = "Pending", task_id: int = None, project_id: int = None):
        if task_id is not None:
            self.id = task_id
            Task._id_counter = max(Task._id_counter, task_id + 1)
        else:
            self.id = Task._id_counter
            Task._id_counter += 1
            
        self.title = title
        self.assigned_to = assigned_to
        self._status = status
        self.project_id = project_id
        
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        self._status = value
        
    def completed(self):
        self._status = "Completed"
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'assigned_to': self.assigned_to,
            'status': self._status,
            'project_id': self.project_id
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data['title'],
            assigned_to=data.get('assigned_to', ''),
            status=data.get('status', 'Pending'),
            task_id=data['id'],
            project_id=data.get('project_id')
        )
        
    def __str__(self):
        assignee = f" - Assigned to: {self.assigned_to}" if self.assigned_to else ""
        return f"[{self.id}] {self.title}{assignee} ({self.status})"