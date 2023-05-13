import glm
import pygame as pg


class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def main_render(self):
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

        # byte_array = self.depth_texture.read()
        # img = pg.image.fromstring(byte_array, glm.ivec2(self.app.WIN_SIZE), 'RGBA', True)
        # pg.image.save(img, '1.png')

    def render(self):
        self.scene.update()
        # pass 1
        self.render_shadow()
        # pass 2
        self.main_render()
        # print(self.app.camera.position, self.app.camera.yaw, self.app.camera.pitch)

    def destroy(self):
        self.depth_fbo.release()

