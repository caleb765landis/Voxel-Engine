import numpy as np

class BaseMesh:
    def __init__(self):
        #OpenGL context
        self.ctx = None

        # shader program
        self.program = None

        self.vbo_format = None

        # attribute names according to the format: ("in_position", "in_color")
        # or attribute names according to the format: ('packed_data',)
        # self.attributes: tuple[str, ...] = ('packed_data',)
        self.attributes: tuple[str, ...] = None

        # vertex array object
        self.vao = None

    def get_vertex_data(self) -> np.array: ...

    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)

        # return vertex array object that is created using a Shader Program and a vertex buffer object
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attributes)], skip_errors=True
        )
        return vao
    
    def render(self):
        self.vao.render()