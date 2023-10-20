import pygame as pg
from Camera import Camera
from settings import *

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)
    
    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def handle_event(self, event):
        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()


    '''
    ------CONTROLS------
    Forward: w
    Backward: s
    Right: d
    Left: a
    Up: e
    Down: q
    Looking: mouse
    '''
    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        velocity = PLAYER_SPEED * self.app.delta_time

        if key_state[pg.K_w]:
            self.move_forward(velocity)
        if key_state[pg.K_s]:
            self.move_back(velocity)
        if key_state[pg.K_d]:
            self.move_right(velocity)
        if key_state[pg.K_a]:
            self.move_left(velocity)
        if key_state[pg.K_e]:
            self.move_up(velocity)
        if key_state[pg.K_q]:
            self.move_down(velocity)
    
    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()

        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)