from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = VBO(app.ctx)
        self.program = ShaderProgram(app.ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube'])

        # shadow cube vao
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube'])

        # ------------------------------------------------- #

        # cube_instanced vao
        self.vaos['cube_instanced'] = self.get_instanced_vao(
            program=self.program.programs['instancing'],
            vbo=self.vbo.vbos['cube'],
            offset_buffer=self.app.instancing_map.offset_buffer,
            prime_buffer=self.app.instancing_map.prime_buffer)

        # shadow cube_instanced vao
        self.vaos['shadow_cube_instanced'] = self.get_instanced_vao(
            program=self.program.programs['shadow_map_instancing'],
            vbo=self.vbo.vbos['cube'],
            offset_buffer=self.app.instancing_map.offset_buffer,
            prime_buffer=self.app.instancing_map.prime_buffer)

        # ------------------------------------------------- #

        # cube_rig vao
        self.vaos['cube_rig'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube_rig'])

        # shadow cube_rig vao
        self.vaos['shadow_cube_rig'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube_rig'])

        # ------------------------------------------------- #

        # cube_rig_instanced vao
        self.vaos['cube_rig_instanced'] = self.get_instanced_vao(
            program=self.program.programs['instancing'],
            vbo=self.vbo.vbos['cube_rig'],
            offset_buffer=self.app.instancing_map.offset_buffer,
            prime_buffer=self.app.instancing_map.prime_buffer)

        # shadow cube_rig_instanced vao
        self.vaos['shadow_cube_rig_instanced'] = self.get_instanced_vao(
            program=self.program.programs['shadow_map_instancing'],
            vbo=self.vbo.vbos['cube_rig'],
            offset_buffer=self.app.instancing_map.offset_buffer,
            prime_buffer=self.app.instancing_map.prime_buffer)

        # ------------------------------------------------- #

        # skybox vao
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def get_instanced_vao(self, program, vbo, offset_buffer, prime_buffer):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs),
                                              (offset_buffer, '3f /i', 'in_offset'),
                                              (prime_buffer, '1f /i', 'in_prime')],
                                    skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()