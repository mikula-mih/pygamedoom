import pygame as pg
import moderngl as mgl
import numpy as np
import sys


class App:
    def __init__(self, win_size=(1920, 1080)):
        pg.init()
        self.WIN_SIZE = win_size

        # opengl settings
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # time objects
        self.clock = pg.time.Clock()
        self.time = 0

        # load shaders
        with open('vertex.glsl') as f:
            vertex = f.read()
        with open('fragment.glsl') as f:
            fragment = f.read()
        self.program = self.ctx.program(vertex_shader=vertex, fragment_shader=fragment)

        # quad screen vbo
        vertices = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (-1, -1, 0), (1, 1, 0)]
        vertex_data = np.array(vertices, dtype='f4')
        self.vbo = self.ctx.buffer(vertex_data)

        # quad vao
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f', 'in_position')])

        # shader uniforms
        self.set_uniform('u_resolution', self.WIN_SIZE)

    def set_uniform(self, u_name, u_value):
        try:
            self.program[u_name] = u_value
        except KeyError:
            pass

    def destroy(self):
        self.vbo.release()
        self.program.release()
        self.vao.release()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
                pg.quit()
                sys.exit()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def update(self):
        self.set_uniform('u_time', self.time)
        self.set_uniform('u_mouse', pg.mouse.get_pos())

    def render(self):
        self.ctx.clear()
        self.vao.render()
        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.update()
            self.render()
            self.clock.tick(0)
            fps = self.clock.get_fps()
            pg.display.set_caption(f'{fps :.1f}')


if __name__ == '__main__':
    App().run()
