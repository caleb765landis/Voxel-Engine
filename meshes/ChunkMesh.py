from meshes.BaseMesh import BaseMesh
from meshes.ChunkMeshBuilder import build_chunk_mesh

class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk

        # vbo format of unsigned 32 bit datatype
        self.vbo_format = '1u4'
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ('packed_data',)
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels = self.chunk.voxels,
            format_size = self.format_size,

            # take into account neighboring chunks
            chunk_pos = self.chunk.position,
            world_voxels = self.chunk.world.voxels
        )
        return mesh
    