from settings import *
from world_objects.Chunk import Chunk
from VoxelHandler import VoxelHandler

class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]

        # all voxels divided into chunks stored into separate numpy array
        # structurally correspond to list of chunks
        # chunks instance will store a pointer to corresponding voxels in this array
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')

        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_handler.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()