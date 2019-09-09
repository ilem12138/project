import pygame
from pygame.locals import *
import sys
import manager
import startscreen


pygame.init()  # 初始化
pygame.mixer.init()
startscreen.showStartScreen()
while True:
 tree = manager.ManagerTree()
 m = manager.Manager(0, 0)
 sound_sign = 0
 world_bgm = pygame.mixer.Sound(manager.SoundPlay.world_bgm)
 game_bgm = pygame.mixer.Sound(manager.SoundPlay.game_bgm)
 while True:
    if m.level == 0:
        if sound_sign == 0:
            game_bgm.stop()
            world_bgm.play(-1)
            sound_sign =1
    else:
        if sound_sign ==1:
            world_bgm.stop()
            game_bgm.play(-1)
            sound_sign = 0
    if m.level ==0:
        tree.draw_tree(m.money)
    else:
        m.set_level_mode(m.level)
        sprite_group = m.draw()
        if m.type ==0:
            m.eliminate_animal()
            m.death_map()
            m.exchange(sprite_group)
        m.judge_level()

    for event in pygame.event.get():
        if event.type ==KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                exit()
        if event.type ==QUIT:
            sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
        m.level,m.money = tree.mouse_select(event, m.level, m.money)
        m.mouse_select(event)

    m.mouse_image()
    pygame.display.flip()

if __name__ == "main":
    main()


