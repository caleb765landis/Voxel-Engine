from settings import *
from ShaderProgram import ShaderProgram
from Scene import Scene
from Player import Player
import moderngl as mgl
import pygame as pg
import sys

class VoxelEngine:
    def __init__(self):
        # init pygame
        pg.init()

        # set up OpenGL
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        # set window resolution and create OpenGL context
        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)

        # enable garbage collection
        self.ctx.gc_mode = 'auto'

        # set up time attributes
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        # lock mouse pointer within window
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        
        # set its position to center of window
        pg.mouse.set_pos([WIN_RES.x / 2, WIN_RES.y / 2])

        # attribute for checking if engine is running
        self.is_running = True

        self.on_init()

    def on_init(self):
        # intitialize player
        self.player = Player(self)
        
        # initialize shader program
        self.shader_program = ShaderProgram(self)

        # initialize scene
        self.scene = Scene(self)

    def update(self):
        # update player
        self.player.update()

        # update shaders
        self.shader_program.update()

        # update scene
        self.scene.update()

        # update time
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001

        # displays fps on window title bar
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')

    def render(self):
        # clear frame and depth buffers
        self.ctx.clear(color=BG_COLOR)

        # render scene
        self.scene.render()

        # draw new frame
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            # check if user is quitting game
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False

    def run(self):
        # while engine is running, handle events, update attributes, and render new values in a new frame
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        # close engine once it stops running
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    app = VoxelEngine()
    app.run()