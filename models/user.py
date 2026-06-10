from models.person import Person

class User(Person):
    _id_counter = 1
    
    def __init__(self, name: str, email: str, user_id: int = None):
        super().__init__(name, email)
        if user_id is not None:
            self.id = user_id
            User._id_counter = max(User._id_counter, user_id + 1)
        else:
            self.id = User._id_counter
            User._id_counter += 1
        self.projects = []
        
    def add_project(self, project):
            self.projects.append(project)
            
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data['name'], email=data['email'], user_id=data['id'])
    
    def __str__(self):
        return f"[{self.id}] {self.name} <{self.email}> - Projects: {len(self.projects)}"