import pygame as pg
import moderngl as mgl
import glm


class Texture:
    def __init__(self, app):  # !!!
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img.png')
        self.textures[1] = self.get_texture(path='textures/img_1.png')
        self.textures[2] = self.get_texture(path='textures/img_2.png')
        self.textures[3] = self.get_texture(path='textures/img_3.png')
        self.textures[4] = self.get_texture(path='textures/img_4.png')
        self.textures['rubik'] = self.get_texture(path='textures/rubik.png')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox2/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture(scale=1)

    def get_depth_texture(self, scale):
        depth_texture = self.ctx.depth_texture(glm.ivec2(self.app.WIN_SIZE) * scale)
        # depth_texture.compare_func = ''
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        # depth_texture.filter = mgl.LINEAR, mgl.LINEAR
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        # texture.fill('orange')
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]