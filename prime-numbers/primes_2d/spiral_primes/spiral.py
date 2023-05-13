import pygame as pg
import numpy as np


def is_prime(num):
    if num == 2: return True
    if num < 2 or not num % 2: return False
    for i in range(3, int(num ** 0.5) + 1, 2):
        if not num % i:
            return False
    return True


class UlamSpiral:
    def __init__(self, size):
        self.size = size if size % 2 else size + 1
        self.max_num = self.size ** 2
        self.arr = np.zeros((self.size, self.size, 3))
        self.pos = np.array([self.size, self.size]) // 2
        self.step = 1
        self.num = 1
        self.primes41 = {i ** 2 + i + 41 for i in range(1000) if is_prime(i ** 2 + i + 41)}
        self.primes17 = {i ** 2 + i + 17 for i in range(1000) if is_prime(i ** 2 + i + 17)}
        self.primes11 = {i ** 2 + i + 11 for i in range(1000) if is_prime(i ** 2 + i + 11)}

    def fill_side(self, iterations, side):
        for i in range(iterations):
            if self.num == self.max_num:
                break
            if self.num in self.primes41:
                self.arr[self.pos[1], self.pos[0]] = (255, 0, 0)
            elif self.num in self.primes17:
                self.arr[self.pos[1], self.pos[0]] = (0, 255, 0)
            elif self.num in self.primes11:
                self.arr[self.pos[1], self.pos[0]] = (0, 0, 255)
            else:
                self.arr[self.pos[1], self.pos[0]] = [255] * 3 if is_prime(self.num) else [0] * 3
            self.pos[side] += self.step if self.step else -self.step
            self.num += 1
        self.step *= -1

    def get_spiral(self):
        for iterations in range(1, self.size * self.size):
            self.fill_side(iterations, 0)
            self.fill_side(iterations, 1)
            self.step *= -1
        return np.rot90(np.flip(self.arr, axis=0), -1)


class SacksSpiral:
    def __init__(self, size):
        self.size = size
        self.max_num = self.size ** 2
        self.arr = np.zeros((2 * self.size, 2 * self.size, 3))
        self.primes41 = {i ** 2 + i + 41 for i in range(1000) if is_prime(i ** 2 + i + 41)}
        self.primes17 = {i ** 2 + i + 17 for i in range(1000) if is_prime(i ** 2 + i + 17)}
        self.primes11 = {i ** 2 + i + 11 for i in range(1000) if is_prime(i ** 2 + i + 11)}

    def get_index(self, num):
        rho = np.sqrt(num)
        phi = 2 * np.pi * rho
        row = int(rho * np.sin(phi)) + self.size
        col = int(rho * np.cos(phi)) + self.size
        return row, col

    def get_spiral(self):
        for num in range(self.max_num):
            if num in self.primes41 and is_prime(num):
                index = self.get_index(num)
                self.arr[index] = (255, 0, 0)
            elif num in self.primes17 and is_prime(num):
                index = self.get_index(num)
                self.arr[index] = (0, 255, 0)
            elif num in self.primes11 and is_prime(num):
                index = self.get_index(num)
                self.arr[index] = (0, 0, 255)
            elif is_prime(num):
                index = self.get_index(num)
                self.arr[index] = (255, 255, 255)
        return np.rot90(self.arr, -1)


class App:
    def __init__(self, res=(1920, 1080)):
        pg.init()
        self.WIDTH, self.HEIGHT = res
        self.screen = pg.display.set_mode(res)
        self.clock = pg.time.Clock()
        self.array_size = 1000

        # self.spiral_array = UlamSpiral(size=self.array_size).get_spiral()
        self.spiral_array = SacksSpiral(size=self.array_size).get_spiral()

        self.spiral = pg.surfarray.make_surface(self.spiral_array)
        self.speed = 5
        self.array_size *= 7
        self.spiral_surface = pg.transform.scale(self.spiral, (self.array_size, self.array_size))
        self.get_pos()

    def get_pos(self):
        self.pos = pg.math.Vector2(self.WIDTH // 2 - self.array_size // 2,
                                   self.HEIGHT // 2 - self.array_size // 2)

    def draw(self):
        self.screen.fill('black')
        self.screen.blit(self.spiral_surface, self.pos)

    def scale(self):
        self.spiral_surface = pg.transform.scale(self.spiral, (self.array_size, self.array_size))

    def control(self):
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_a]:
            self.pos[0] += self.speed
        if pressed_keys[pg.K_d]:
            self.pos[0] -= self.speed
        if pressed_keys[pg.K_w]:
            self.pos[1] += self.speed
        if pressed_keys[pg.K_s]:
            self.pos[1] -= self.speed
        if pressed_keys[pg.K_UP]:
            self.array_size *= 1.1
            self.array_size = min(self.array_size, 20000)
            self.scale()
            self.get_pos()
        if pressed_keys[pg.K_DOWN]:
            self.array_size //= 1.1
            self.scale()
            self.get_pos()

    def update(self):
        pg.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            [exit() for i in pg.event.get() if i.type == pg.QUIT
             or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE)]
            self.control()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()