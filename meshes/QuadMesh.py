from settings import *
from meshes.BaseMesh import BaseMesh

class QuadMesh(BaseMesh):
    def __init__(self, app):
        # use BaseMesh's constructor
        super().__init__()

        # initialize predefined attributes
        self.app = app
        self.ctx = app.ctx
        self.program = app.shader_program.quad
        # vertex buffer data in form of 3 floats for vertex data and 3 floats for color
        self.vbo_format = '3f 3f'
        self.attrs = ('in_position', 'in_color')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        # vertices of two triangles, with counter-clockwise traversal
        # these vertices for each triangle will combine to make a quad
        vertices = [
            (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0),
            (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0)
        ]

        # vertex colors
        colors = [
            (0, 1, 0), (1, 0, 0), (1, 1, 0),
            (0, 1, 0), (1, 1, 0), (0, 0, 1)
        ]

        # vertex data in form of numpy float32 rray
        vertex_data = np.hstack([vertices, colors], dtype='float32')
        return vertex_data