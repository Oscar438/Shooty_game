import pygame
import Game_Functions as Game
import Entity as Ent
import sys
import random

pygame.init()
SCREEN_HIEGHT = 750
SCREEN_WIDTH = 1000
TICK = 30

clock = pygame.time.Clock()

p_colour = (0, 150, 150)
b_colour = (200, 100, 0)
e_colour = (255, 0, 50)
boss_colour = (255, 0, 0)
gun_colour = (255, 255, 150)
t_colour = (255, 255, 255)
p_point = (SCREEN_WIDTH // 2, SCREEN_HIEGHT // 2)
p_size = 20
p_reload = 0
b_rate = 10
b_size = 5
b_speed = 3
e_size = 10
e_speed = 3
boss_size = 15
boss_speed = 2
bullet_count_max = 25
enemy_count_max = 10
boss_list = []
boss = False
score = 0

# for ii in range(bullet_count_max):
# 	bullet_list.append([])


# for ii in range(enemy_count_max):
# 	enemy_list.append([])

# I prefer list comprehensions whenever possible
bullet_list = [list() for i in range(bullet_count_max)]
enemy_list = [list() for i in range(enemy_count_max)]

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HIEGHT])

the_font = pygame.font.SysFont("momospace", 35)

player = Ent.player(screen, p_colour, gun_colour, p_point, p_size)

Game_Over = False

# The standard way of writing a main() function in python is doing this weird thing.
# It's what separates 'code' from 'scripts'
if __name__ == '__main__':
    while not Game_Over:
        events = pygame.event.get()
        if any([event.type for event in events if event.type == pygame.QUIT]):
            Game_Over = True

        if events:
            event = events[0]
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                shoot = False

        # Fill the background
        screen.fill((0, 0, 0))

        # Draw a player triangle point to mouse
        mouse_position = pygame.mouse.get_pos()
        gun_point = player.draw_player(mouse_position)



        if pygame.key.get_pressed()[32] == 1:
            if p_reload == 0:
                new_bullet = Ent.projectile(screen, b_colour, gun_point, b_size, p_point, pygame.mouse.get_pos(),
                                            b_speed, bullet_count_max)
                bullet_list[new_bullet.count] = new_bullet
                p_reload = b_rate

        for ii in range(len(bullet_list)):
            if bullet_list[ii] != []:
                bullet_list[ii].draw_projectile()
                bullet_list[ii].update_projectiles()

        for ii in range(len(enemy_list)):
            if enemy_list[ii] == [] and random.random() < 0.01:
                new_enemy = Ent.enemy(screen, e_colour, e_size, p_point, e_speed, SCREEN_WIDTH, SCREEN_HIEGHT,
                                      enemy_count_max)
                enemy_list[new_enemy.count] = new_enemy

            for jj in range(len(bullet_list)):
                if enemy_list[ii] != [] and bullet_list[jj] != []:
                    if Game.dist(bullet_list[jj].point, enemy_list[ii].point, b_size + e_size):
                        bullet_list[jj] = []
                        enemy_list[ii] = []
                        score += 1
                        if score % 10 == 9:
                            boss = True

            if enemy_list[ii] != []:
                if Game.dist(player.point, enemy_list[ii].point, p_size + e_size):
                    Game_Over = True
                    break
                enemy_list[ii].draw_projectile()
                enemy_list[ii].update_projectiles()

        for jj in range(len(bullet_list)):
            if boss_list != [] and bullet_list[jj] != []:
                if Game.dist(bullet_list[jj].point, boss_list.point, b_size + boss_size):
                    bullet_list[jj] = []
                    if boss_list.hp != 1:
                        boss_list.hp -= 1
                    else:
                        boss_list = []
                        score += 1
                        buff = random.randint(0, 2)
                        if buff == 0:
                            b_speed += 1
                        elif buff == 1:
                            b_size += 1
                        else:
                            if b_rate == 1:
                                b_speed += 1
                            else:
                                b_rate -= 1

                        if score % 10 == 9:
                            boss = True
        if boss_list != []:
            if Game.dist(player.point, boss_list.point, p_size + boss_size):
                Game_Over = True
                break
            boss_list.draw_projectile()
            boss_list.update_projectiles()

        if boss and boss_list == []:
            print('boss')
            print(Ent.boss.Boss_count)
            boss_list = Ent.boss(screen, boss_colour, boss_size + Ent.boss.Boss_count * 2, p_point,
                                 boss_speed + Ent.boss.Boss_count, SCREEN_WIDTH, SCREEN_HIEGHT, enemy_count_max)
            enemy_count_max += 1
            enemy_list.append([])

        score_text = "Score: " + str(score)
        label = the_font.render(score_text, 1, t_colour)
        screen.blit(label, (SCREEN_WIDTH - 200, SCREEN_HIEGHT - 40))

        if p_reload > 0:
            p_reload -= 1

        # Flip the display
        pygame.display.flip()
        clock.tick(TICK)

    pygame.quit()
    print(score)
