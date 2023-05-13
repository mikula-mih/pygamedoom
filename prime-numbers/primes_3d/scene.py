from model import *


def is_prime(num):
    if num == 2 or num == 3: return True
    if num < 2 or not num % 2: return False
    for i in range(3, int(num ** 0.5 + 1), 2):
        if not num % i:
            return False
    return True


class InstancingMap:
    def __init__(self, app):
        self.app = app
        self.num_instances = None
        self.offset_buffer, self.prime_buffer = None, None
        self.get_data()

    def get_data(self, nums=3000):
        positions, primes = [], []
        pos = glm.vec3(0, 0, 0)

        directions = {0: glm.vec3(1, 0, 0), 1: glm.vec3(0, 1, 0), 2: glm.vec3(0, 0, 1),
                      3: glm.vec3(-1, 0, 0), 4: glm.vec3(0, -1, 0), 5: glm.vec3(0, 0, -1)}
        found_primes = 0
        color_seed = 1
        for num in range(nums):
            direction = directions[found_primes % 6]
            pos = glm.vec3(pos + direction)
            positions.append(pos)

            if is_prime(num):
                color_seed = num
                found_primes += 1
                primes.append(-1)
            else:
                primes.append(color_seed)

        self.num_instances = nums
        self.offset_buffer = self.app.ctx.buffer(np.array(positions, dtype='f4'))
        self.prime_buffer = self.app.ctx.buffer(np.array(primes, dtype='f4'))


    # def get_data(self):
    #     positions, primes = [], []
    #     # WIDTH, HEIGHT, DEPTH = 64, 64, 64
    #     WIDTH, HEIGHT, DEPTH = 44, 44, 44
    #
    #     for x in range(WIDTH):
    #         for y in range(HEIGHT):
    #             for z in range(DEPTH):
    #
    #                 # num = 2 * (x ^ y ^ z)
    #                 num = x ^ y | z
    #
    #                 if is_prime(num):
    #                     positions.append((x, y, z))
    #                     primes.append(num + 1)
    #
    #     self.num_instances = len(positions)
    #     self.offset_buffer = self.app.ctx.buffer(np.array(positions, dtype='f4'))
    #     self.prime_buffer = self.app.ctx.buffer(np.array(primes, dtype='f4'))


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.instance_counter = 0
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # self.cube_instanced = CubeRigInstanced(app, num_instances=self.app.instancing_map.num_instances,
        #                                       tex_id='rubik')
        self.cube_instanced = CubeRigInstanced(app, num_instances=self.app.instancing_map.num_instances,
                                              tex_id=3)
        # self.cube_instanced = CubeInstanced(app, num_instances=self.app.instancing_map.num_instances,
        #                                     tex_id=1)
        add(self.cube_instanced)

    def update(self):
        if self.app.instancing_map.num_instances > self.instance_counter:
            self.instance_counter += 1
            self.cube_instanced.num_instances = self.instance_counter

