import pygame
import Game_Functions as Game
import sys
import random
from constants import Colours, Sizes, Speeds


class Entity:
    def __init__(self, screen, colour, point, radius):
        self.delta_y = 0
        self.delta_x = 0
        self.screen = screen
        self.colour = colour
        self.point = point
        self.radius = radius

    def draw_projectile(self):
        pygame.draw.circle(self.screen, self.colour, self.point, self.radius)

    def update_projectiles(self):
        self.point_true = (self.point_true[0] + self.delta_x, self.point_true[1] + self.delta_y)
        self.point = (int(self.point_true[0] + self.delta_x), int(self.point_true[1] + self.delta_y))


class Player(Entity):
    def __init__(self, screen, colour, gun_colour, point, radius):
        super().__init__(screen, colour, point, radius)
        self.gun_colour = gun_colour

    def draw_player(self, mouse):
        slope = Game.gradient(self.point, mouse)
        r_slope = Game.r_gradient(self.point, mouse)

        p1 = Game.tri_peak(self.point, slope, 2.5 * self.radius, mouse)
        p2 = Game.tri_peak(self.point, -r_slope, self.radius, mouse)
        p3 = (2 * self.point[0] - p2[0], 2 * self.point[1] - p2[1])
        pygame.draw.polygon(self.screen, self.gun_colour, [p1, p2, p3])
        pygame.draw.circle(self.screen, self.colour, self.point, self.radius)
        return (int(p1[0]), int(p1[1]))

    def update_player(self):
        pass


class Projectile(Entity):
    count = 0

    def __init__(self, screen, colour, point, radius, start_point, ref_point, speed, max_bullets):
        super().__init__(screen, colour, point, radius)
        self.point_true = point
        self.speed = speed
        self.delta_x, self.delta_y = Game.delta(start_point, ref_point, speed)
        self.count = Projectile.count
        Projectile.count = (Projectile.count + 1) % max_bullets


class Enemy(Entity):
    def __init__(self, screen: pygame.Surface, id_number, colour=Colours.enemy_colour,
                 radius=Sizes.enemy_size, speed=Speeds.enemy_speed):
        """
        We mus pass in the screen argument, however the others will use the default values
        that are outlined in constants.py

        :param screen: The screen on which to draw our enemy
        :param colour: The colour of the enemy
        :param radius: The radios of the enemy
        :param speed: The speed of the enemy
        """
        self.id_number = id_number
        self.size = radius
        width, height = screen.get_size()
        ref_point = (width // 2, height // 2)
        super().__init__(screen, colour, ref_point, radius)
        x = random.choice([True, False])
        y = random.choice([True, False])
        r = random.random()
        if x + y:
            if not x:
                point = (r * width, -50)
            elif not y:
                point = (r * width, 50 + height)
            else:
                point = (-50, r * height)
                pass
        else:
            point = (50 + width, r * height)

        self.point = (int(point[0]), int(point[1]))
        self.point_true = point
        self.delta_x, self.delta_y = Game.delta(point, ref_point, speed)


class Boss(Enemy):
    Boss_count = 0

    def __init__(self, screen, colour, radius, speed):
        super(Boss).__init__(screen, colour, radius, speed)
        self.hp = Boss.Boss_count + 1
        Boss.Boss_count += 1


class EnemyCollection:
    def __init__(self, max_enemies, screen):
        self.enemy_list = [Enemy(screen, i) for i in range(max_enemies)]

    def count(self):
        return len(self.enemy_list)

    def add_enemy(self, screen):
        id_number = self.count() + 1
        self.enemy_list.append(Enemy(screen, id_number))

    def remove_enemy(self, enemy: Enemy):
        self.enemy_list.pop(enemy.id_number)

    def detect_collision(self, target):
        for enemy in self.enemy_list:
            Game.dist(target.point, enemy.point, enemy.size + target.size)
