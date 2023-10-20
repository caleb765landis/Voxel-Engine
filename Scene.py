from settings import *
from meshes.QuadMesh import QuadMesh
from World import World
from world_objects.VoxelMarker import VoxelMarker

class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(self.app)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)

    def update(self):
        self.world.update()
        self.voxel_marker.update()

    def render(self):
        self.world.render()
        self.voxel_marker.render()