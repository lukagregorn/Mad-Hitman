# basic instance

class Instance():

    _type = "Instance"

    def __init__(self, name="Instance", position=[0.0,0.0], rotation=0.0):
        self.name = name
        self.position = position
        self.rotation = rotation

    def _update(self, dt):
        pass