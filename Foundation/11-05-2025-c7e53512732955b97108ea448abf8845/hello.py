class Person:
    def __init__(self, name):
        self.name = name
        
    
    def __repr__(self):
        """
        Return a string representation of the Person object in the format: Person('<name>').
        This is useful for debugging and development purposes.
        """
        return f"Person('{self.name}')"
    
# Person("Monal")