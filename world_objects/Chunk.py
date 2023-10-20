from settings import *
from meshes.ChunkMesh import ChunkMesh
import random

class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.app.player.frustum.is_on_frustum

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model
    
    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        # if any voxel exists in this chunk, render the chunk
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        # create an empty chunk
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')

        # rest of method fills chunk

        # chunk position
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        rng = random.randrange(1, 100)

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                # start getting world positions of chunk relative to other chunks
                wx = x + cx
                wz = z + cz

                # uses simplex function for 3d noise when filling voxels
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 2

        # if any voxels exits in this chunk, the chunk is not empty
        if np.any(voxels):
            self.is_empty = False
                
        return voxels