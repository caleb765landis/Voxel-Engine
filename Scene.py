from settings import *
from meshes.QuadMesh import QuadMesh
from World import World

class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(self.app)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()