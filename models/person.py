class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value: str):
        if '@' not in value:
            raise ValueError("Invalid email address.")
        self._email = value.strip()
        
    def __repr__(self):
            return f"{self.__class__.__name__}(name={self.name!r}, email={self.email!r})"
