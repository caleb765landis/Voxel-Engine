from settings import *
from meshes.QuadMesh import QuadMesh
from world_objects.Chunk import Chunk

class Scene:
    def __init__(self, app):
        self.app = app
        self.chunk = Chunk(self.app)

    def update(self):
        pass

    def render(self):
        self.chunk.render()