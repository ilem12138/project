import pygame
import random
from pygame.locals import *
import startscreen


Window_Width = 1000  
Window_Height = 600
White = (255, 255, 255)  
Black = (0, 0, 0)  
Red = (255, 0, 0)   
Green = (0, 255, 0)  
DARKGreen = (0, 155, 0)  
DARKGRAY = (40, 40, 40)     
YELLOW = (255, 255, 0)  
Red_DARK = (150, 0, 0)  
BLUE = (0, 0, 255)  
BLUE_DARK = (0, 0, 150)  
  
  
BGCOLOR = White

def checkForKeyPress():  
    if len(pygame.event.get(QUIT)) > 0:  
        terminate()  
    keyUpEvents = pygame.event.get(KEYUP)  
    if len(keyUpEvents) == 0:  
        return None  
    if keyUpEvents[0].key == K_ESCAPE:  
        terminate()  
    return keyUpEvents[0].key

def terminate():  
    pygame.quit()  
    sys.exit()


class SoundPlay:
    game_bgm = "sound/GameSceneBGM.ogg"
    world_bgm = 'sound/WorldSceneBGM.ogg'
    eliminate = ('sound/eliminate1.ogg', 'sound/eliminate2.ogg', 'sound/eliminate3.ogg', 'sound/eliminate4.ogg',\
                 'sound/eliminate5.ogg')  # 消除声音
    score_level = ('sound/good.ogg', 'sound/great.ogg', 'sound/amazing.ogg', 'sound/excellent.ogg',\
                   'sound/unbelievable.ogg')   # 得分声音
    click = "sound/click.bubble.ogg"  # 点击选中声音
    board_sound = 'sound/board.ogg'   # 落板子声音
    click_button = 'sound/click_common_button.ogg'  # 点击按钮声音
    money_sound = 'sound/money.ogg'   # 点击银币声音
    ice_break = 'sound/ice_break.ogg'   # 冰消除声音
    energy_sound = 'sound/boom.ogg'
    def __init__(self, filename, loops=0):
        self.sound = pygame.mixer.Sound(filename)
        self.sound.play(loops)



class Tree(pygame.sprite.Sprite):
    """树类"""
    tree = 'pic2/tree.png'  
    fruit = r'pic2/fruit.png' 
    money = 'pic2/money.png'
    mark = 'pic2/question.png'

    x, y = 340, 510
    h = 90
    position = ([x-200, y-360], [x-120, y-240], [x-180, y-70], [x+35, y-h-65], [x+125, y-25-h+50], [x+235, y-95-h],[x+370, y-h*2+45], [x+420, y-h*3-85])  
    mark_position = (28,225)
    def __init__(self, icon, position):
        super().__init__()
        self.image = pygame.image.load(icon).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position      # 左下角为坐标

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ManagerTree:
    """管理树类"""
    __screen_size = (900, 600) 
    screen = pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    fruit_list = []
    fruit_image = pygame.image.load(Tree.fruit).convert_alpha()
    mark_image = pygame.image.load(Tree.mark).convert_alpha()
    fruit_width = fruit_image.get_width()
    fruit_height = fruit_image.get_height()
    mark_width = mark_image.get_width()
    type = 0  
    money_empty = False  # 银币不足

    def load_text(self, text, position, txt_size=25, txt_color=(255, 255, 255)):
        my_font = pygame.font.SysFont(None, txt_size)
        text_screen = my_font.render(text, True, txt_color)
        self.screen.blit(text_screen, position)

    def draw_tree(self,money_num):
        Tree(Tree.tree, (0, 600)).draw(self.screen)      
        Tree(Tree.money, (15, 165)).draw(self.screen)# 画银币
        Tree(Tree.mark, (28, 225)).draw(self.screen)
        self.load_text(str(money_num), (32, 154), 21)
        for i in range(0, 8):                          
            Tree(Tree.fruit, Tree.position[i]).draw(self.screen)
            self.load_text(str(i+1), (Tree.position[i][0]+15, Tree.position[i][1]-47))
        if self.type == 1:

            if self.money_empty:
                self.load_text("money is not enough!", (300, 310), 50, White)
                pygame.display.flip()
                pygame.time.delay(500)
                self.money_empty = False

    def mouse_select(self, button, level, money_num):
        """鼠标点击"""
        if button.type == MOUSEBUTTONDOWN:
            mouse_down_x, mouse_down_y = button.pos
            if level == 0:
                if self.type == 0:          
                    for i in range(0, 8):
                        if Tree.position[i][0] < mouse_down_x < Tree.position[i][0] + self.fruit_width \
                                and Tree.position[i][1] - self.fruit_height < mouse_down_y < Tree.position[i][1]:
                            
                                level = i + 1
                    if Tree.mark_position[0]-5 < mouse_down_x < Tree.mark_position[0]+self.mark_width\
                        and Tree.mark_position[1]-25 < mouse_down_y < Tree.mark_position[1]+self.mark_width:
                        startscreen.introduceScreen()
        if button.type == MOUSEBUTTONUP:
            pass
        return level, money_num


class Element(pygame.sprite.Sprite):
    """ 元素类 """
    # 图标元组，包括6个小动物，
    animal = ('pic2/fox.png', 'pic2/bear.png', 'pic2/chick.png', 'pic2/eagle.png', 'pic2/frog.png', 'pic2/cow.png')
    brick = 'pic2/brick.png'  
    frame = 'pic2/frame.png'
    ice = 'pic2/ice0.png'  # 冰层
    bling = ("pic2/bling1.png", "pic2/bling2.png", "pic2/bling3.png", "pic2/bling4.png", "pic2/bling5.png",\
             "pic2/bling6.png", "pic2/bling7.png", "pic2/bling8.png", "pic2/bling9.png")   # 消除动画

    ice_eli = ('pic2/ice0.png', 'pic2/ice1.png', 'pic2/ice2.png', 'pic2/ice3.png', 'pic2/ice4.png', 'pic2/ice5.png',\
               'pic2/ice6.png', 'pic2/ice7.png', 'pic2/ice8.png')    # 消除冰块动画
    # 得分图片
    score_level = ('pic2/good.png', 'pic2/great.png', 'pic2/amazing.png', 'pic2/excellent.png', 'pic2/unbelievable.png')
    none_animal = 'pic2/noneanimal.png'        
    stop = 'pic2/exit.png'       # 暂停键
    stop_position = (20, 530)
    refresh= 'pic2/refresh.png'       # 暂停键
    refresh_position = (810, 530)
    energy = 'pic2/energy.png'
    energy_position = (720,530)
    question ='pic2/question.png'
    question_position = (28,197)
    voice ='pic2/voice.png'
    voice_position = (110,530)
    def __init__(self, icon, position):
        super().__init__()
        self.image = pygame.image.load(icon).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position         # 左上角坐标
        self.speed = [0, 0]
        self.init_position = position

    def move(self, speed):
        self.speed = speed
        self.rect = self.rect.move(self.speed)
        if self.speed[0] != 0:    # 如果左右移动
            if abs(self.rect.left-self.init_position[0]) == self.rect[2]:
                self.init_position = self.rect.topleft
                self.speed = [0, 0]
        else:
            if abs(self.rect.top-self.init_position[1]) == self.rect[3]:
                self.init_position = self.rect.topleft
                self.speed = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Board(pygame.sprite.Sprite):
    step_board = 'pic2/step.png'              # 剩余步数板子
    step = ('pic2/0.png', 'pic2/1.png', 'pic2/2.png', 'pic2/3.png', 'pic2/4.png', 'pic2/5.png',\
            'pic2/6.png', 'pic2/7.png', 'pic2/8.png', 'pic2/9.png', )
    task_board = 'pic2/task.png'              # 任务板子
    ok = 'pic2/ok.png'    
    # 关数板子
    levelBoard = ('pic2/level0.png', 'pic2/level1.png', 'pic2/level2.png', 'pic2/level3.png', 'pic2/level4.png', 'pic2/level5.png',
                  'pic2/level6.png', 'pic2/level7.png', 'pic2/level8.png', 'pic2/level9.png', 'pic2/level10.png')
    # xxx = 'pic2/x.png'  
    test = 'pic2/test.png'
    success_board = 'pic2/successtest1.png'  # 过关成功板子
    fail_board = 'pic2/failBoard.png'  # 任务失败
    step_add = 'pic2/step_add.png'  # 增加步数
    next = "pic2/next.png"  # 下一关按钮
    replay = "pic2/replay.png"  # 重玩图片
    stars = 'pic2/startest.png'  # 星星图片
    money = 'pic2/money.png'  # 银币
    button_position = [[275, 475], [495, 475]]
    starts_position = [[280+47, 335], [375+35, 335], [460+32, 335]]

    def __init__(self, icon, position):
        super().__init__()
        self.image = pygame.image.load(icon).convert_alpha()
        self.speed = [0, 45]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position                  # 左下角为坐标值

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.bottom >= 543:
            self.speed = [0, -45]
        if self.speed == [0, -45] and self.rect.bottom <= 450:
            self.speed = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Manager:
    """  数组类 """
    __screen_size = (900, 600)
    screen = pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    __brick_size = 50
    __bg = pygame.image.load('pic2/bg.png').convert()
    stop_width = 63
    refresh_width = 63
    energy_width = 60
    question_width = 28
    voice_width = 63
    selected = [-1, -1]   # 现选中[row, col]
    exchange_sign = -1  # 未交换标志
    last_sel = [-1, -1]  # 上一次选中[row, col]
    change_value_sign = False  # 是否交换值标志，初始不交换
    death_sign = True  # 死图标志，初始不是死图
    boom_sel = [-1, -1]   
    level = 0  
    money = 100  # 金币
    energy_num = 0
    num_sign = True
    type = 2  
    reset_mode = True     # 是否重新布局（每关布局）
    init_step = 15  # 每关规定步数
    step = init_step     # 代表游戏所剩余的步数
    score = 0        # 得数
    min = 20  # 分数中间值1
    max = 50  # 分数中间值2
    animal_num = [0, 0, 0, 0, 0, 0]   # 本关消除各小动物的个数
    ice_num = 0
    success_board = Board(Board.success_board, [200, 0])  # 过关成功板
    fail_board = Board(Board.fail_board, [200, 0])  # 任务失败板
    height, width = 9, 9
    row, col = 5, 5
    animals = [0,1,2,3,4,5]
    random.shuffle(animals)
    choose = random.sample(range(0,5), 2)
    ice_list = [[-1 for col in range(21)]for row in range(21)]   # -1不画，1画冰
    animal = [[-1 for col in range(21)]for row in range(21)]  
    list_x, list_y = (__screen_size[0] - 11 * __brick_size) / 2, (__screen_size[1] - 11 * __brick_size) / 2  # 矩阵坐标

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.list_x = (Manager.__screen_size[0] - self.width * Manager.__brick_size) / 2
        self.list_y = (Manager.__screen_size[1] - self.height * Manager.__brick_size) / 2
        self.row, self.col = Manager.xy_rc(self.list_x, self.list_y)
        self.list_x, self.list_y = Manager.rc_xy(self.row, self.col)
        self.ice_list = [[-1 for col in range(21)]for row in range(21)]
        self.animal = [[-1 for col in range(21)]for row in range(21)]
        self.reset_animal()

    def reset_animal(self):
        for row in range(self.row, self.row + self.height):
            for col in range(self.col, self.col + self.width):
                self.animal[row][col] = random.randint(0, 5)

    @staticmethod
    def rc_xy(row, col):
        """row col 转 x，y坐标"""
        return int(Manager.list_x + (col-Manager.col)*Manager.__brick_size), int\
            (Manager.list_y+(row-Manager.row)*Manager.__brick_size)

    @staticmethod
    def xy_rc(x, y):
        """x，y坐标转row col"""
        return int((y-Manager.list_y)/Manager.__brick_size+Manager.row), int\
            ((x-Manager.list_x)/Manager.__brick_size+Manager.col)

    @staticmethod
    def draw_brick(x, y):
        brick = Element(Element.brick, (x, y))
        Manager.screen.blit(brick.image, brick.rect)

    def draw_task(self, task_animal_num, which_animal, \
                  board_position=(400, 95), animal_position=(430, 15), txt_position=(470, 45)):
        """画任务板子"""
        txt_size = 24
        txt_color = (0, 0, 0)
        Board(Board.task_board, board_position).draw(self.screen)
        if which_animal == 6:
            task_animal = Element(Element.ice, animal_position)
        else:
            task_animal = Element(Element.animal[which_animal], animal_position)
        task_animal.image = pygame.transform.smoothscale(task_animal.image, (40, 40))
        task_animal.draw(self.screen)
        if which_animal == 6:
            if task_animal_num-self.ice_num <= 0:
                Board(Board.ok, (txt_position[0], txt_position[1]+15)).draw(self.screen)
            else:
                self.load_text(str(task_animal_num-self.ice_num), txt_position, txt_size, White)
        else:
            if task_animal_num - self.animal_num[which_animal] <= 0:
                Board(Board.ok, (txt_position[0], txt_position[1]+15)).draw(self.screen)
            else:
                self.load_text(str(task_animal_num - self.animal_num[which_animal]), txt_position, txt_size, White)

    def draw(self):
      if self.level != 0:
        self.screen.blit(Manager.__bg, (0, 0))                    
        Board(Board.step_board, (0, 142)).draw(self.screen)       
        tens = self.step//10  
        single = self.step % 10  
        if tens == 0:
            Board(Board.step[single], (765, 85)).draw(self.screen)
        else:
            Board(Board.step[tens], (750, 85)).draw(self.screen)
            Board(Board.step[single], (771, 85)).draw(self.screen)   
        Board(Board.levelBoard[self.level], (30, 105)).draw(self.screen)
        Tree(Tree.money, (15, 165)).draw(self.screen)  # 画银币
        self.load_text(str(self.money), (32, 154), 21)
        Element(Element.stop, Element.stop_position).draw(self.screen)
        Element(Element.refresh, Element.refresh_position).draw(self.screen)
        Element(Element.energy, Element.energy_position).draw(self.screen)
        Element(Element.question, Element.question_position).draw(self.screen)
        BrickGroup = pygame.sprite.Group()
        AnimalGroup = pygame.sprite.Group()
        IceGroup = pygame.sprite.Group()
        for i in range(0, 21):
            for j in range(0, 21):
                x, y = Manager.rc_xy(i, j)
                if self.animal[i][j] != -1:
                    BrickGroup.add(Element(Element.brick, (x, y)))
                    AnimalGroup.add(Element(Element.animal[self.animal[i][j]], (x, y)))
                if self.ice_list[i][j] != -1:
                    IceGroup.add(Element(Element.ice, (x, y)))
        BrickGroup.draw(self.screen)                                                         # 砖
        IceGroup.draw(self.screen)                                                     
        for animallist in AnimalGroup:
            self.screen.blit(animallist.image, animallist.rect)                           
        if self.level == 1:
            self.draw_task(10, self.animals[0])
        elif self.level == 2:
            self.draw_task(21, self.animals[1])
        elif self.level == 3:
            self.draw_task(16, self.animals[2], (300, 95), (330, 15), (360, 45))
            self.draw_task(16, self.animals[3] , (500, 95), (530, 15), (560, 45))
        elif self.level == 4:
            self.draw_task(18, self.animals[4], (300, 95), (330, 15), (360, 45))
            self.draw_task(18, self.animals[5], (500, 95), (530, 15), (560, 45))
        elif self.level == 5:
            self.draw_task(28, self.animals[self.choose[0]] , (300, 95), (330, 15), (360, 45))
            self.draw_task(28, self.animals[self.choose[1]], (500, 95), (530, 15), (560, 45))
        elif self.level == 6:
            self.draw_task(15, 6)
        elif self.level == 7:
            self.draw_task(49, 6)        
        else :
            self.draw_task(40, 6)


        if self.selected != [-1, -1]:
            frame_sprite = Element(Element.frame, Manager.rc_xy(self.selected[0], self.selected[1]))
            self.screen.blit(frame_sprite.image, frame_sprite.rect)                        

        self.load_text('score:' + str(self.score), (300, 550), 24)
        self.load_text('energy:' + str(self.energy_num), (430, 550), 24)
        pygame.draw.rect(self.screen,White, Rect(300, 570, self.score%100*2 , 25))
        pygame.draw.rect(self.screen, Black, Rect(300, 570, 200, 25), 2)
        
        return AnimalGroup

    def mouse_image(self):
        """"  更换鼠标图片 """
        mouse_cursor = pygame.image.load('pic2/mouse.png').convert_alpha()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        # 计算光标的左上角位置
        mouse_x -= mouse_cursor.get_width() / 2
        mouse_y -= mouse_cursor.get_height() / 2
        self.screen.blit(mouse_cursor, (mouse_x, mouse_y))

    def mouse_select(self, button):
        """鼠标点击"""
        if button.type == MOUSEBUTTONDOWN:
            mouse_down_x, mouse_down_y = button.pos
            if self.type == 1:                                                       # 过关成功
                if Board.button_position[0][0] < mouse_down_x < Board.button_position[0][0]+100 \
                        and Board.button_position[0][1]-50 < mouse_down_y < Board.button_position[0][1]:  # 点击再来一次按钮
                    
                    self.reset_mode = True
                elif Board.button_position[1][0] < mouse_down_x < Board.button_position[1][0]+100 \
                        and Board.button_position[1][1]-50 < mouse_down_y < Board.button_position[1][1]:  # 点击下一关按钮
                    if self.level==8:
                        self.load_text("This is the last level!", (300, 310), 50, White)
                        pygame.display.flip()
                        pygame.time.delay(800)
                        self.level+=0
                        self.reset_mode = True
                    else:    
                     self.level += 1                                                   # 关卡数加一
                     self.reset_mode = True
                elif 610 < mouse_down_x < 610 + 55 and 205 - 55 < mouse_down_y < 205: 
                    self.level = 0
                    self.reset_mode = True

            elif self.type == -1:                                                    # 过关失败
                if Board.button_position[1][0] < mouse_down_x < Board.button_position[1][0]+100 \
                        and Board.button_position[1][1]-50 < mouse_down_y < Board.button_position[1][1]:  # 点击再来一次按钮
                    
                    self.reset_mode = True
                elif Board.button_position[0][0] < mouse_down_x < Board.button_position[0][0]+100 \
                        and Board.button_position[0][1]-50 < mouse_down_y < Board.button_position[0][1]:   # 点击再来5步按钮
                    if self.money < 50:
                        self.load_text("money is not enough!", (300, 310), 50, White)
                        pygame.display.flip()
                        pygame.time.delay(800)                               
                    else:
                        self.money -= 50
                        self.step += 50
                        self.type = 0                           # 游戏中
                        self.fail_board = Board(Board.fail_board, [200, 0])
                elif 610 < mouse_down_x < 610 + 55 and 205 - 55 < mouse_down_y < 205:   
                    self.level = 0
                    self.reset_mode = True

            elif self.type == 0:
                if self.list_x < mouse_down_x < self.list_x + Manager.__brick_size * self.width \
                        and self.list_y < mouse_down_y < self.list_y + Manager.__brick_size * self.height:
                    mouse_selected = Manager.xy_rc(mouse_down_x, mouse_down_y)
                    if self.animal[mouse_selected[0]][mouse_selected[1]] != -1:
                        SoundPlay(SoundPlay.click)
                        self.selected = mouse_selected
                        if (self.last_sel[0] == self.selected[0] and abs(self.last_sel[1] - self.selected[1]) == 1) \
                                or (self.last_sel[1] == self.selected[1] and abs(self.last_sel[0] - self.selected[0]) == 1):
                            self.exchange_sign = 1             
                elif Element.stop_position[0] < mouse_down_x < Element.stop_position[0]+self.stop_width\
                        and Element.stop_position[1] < mouse_down_y < Element.stop_position[1]+self.stop_width:   
                    SoundPlay(SoundPlay.click_button)
                    self.level = 0
                    self.reset_mode = True
                elif Element.refresh_position[0] < mouse_down_x < Element.refresh_position[0]+self.refresh_width\
                        and Element.refresh_position[1] < mouse_down_y < Element.refresh_position[1]+self.refresh_width:
                   if self.money < 50:
                      self.load_text("money is not enough!", (300, 310), 50, White)
                      pygame.display.flip()
                      pygame.time.delay(800)
                   else:
                     self.money -= 50
                     self.fail_board = Board(Board.fail_board, [200, 0])
                     SoundPlay(SoundPlay.click_button)
                     pygame.time.delay(500)
                     Element(Element.none_animal, (230, 100)).draw(self.screen)
                     pygame.display.flip()
                     pygame.time.delay(800)
                     temp = [self.step, self.score, self.animal_num, self.ice_num]
                     self.reset_mode = True
                     if self.level<6:
                         self.set_level_mode(self.level)
                     else:
                         self.set_level_mode_x(self.level)
                     self.step = temp[0]
                     self.score = temp[1]
                     self.animal_num = temp[2]
                     self.ice_num =temp [3]
                elif Element.energy_position[0] < mouse_down_x < Element.refresh_position[0]+self.energy_width\
                        and Element.energy_position[1] < mouse_down_y < Element.energy_position[1]+self.energy_width:
                   if self.energy_num < 1:
                      self.load_text("energy is not enough!", (300, 310), 50, White)
                      pygame.display.flip()
                      pygame.time.delay(800)
                   else:
                     self.energy_num -= 1
                     self.fail_board = Board(Board.fail_board, [200, 0])
                     SoundPlay(SoundPlay.click_button)
                     pygame.time.delay(500)
                     SoundPlay(SoundPlay.energy_sound)
                     line=random.randint(self.row, self.row+self.height)
                     for j in range(self.col, self.col+self.width):  
                       if self.animal[line][j] != -1 :
                          self.animal[line][j]=-2
                          self.score+1
                     self.fall_animal() 
                elif Element.question_position[0] < mouse_down_x < Element.question_position[0]+self.question_width\
                        and Element.question_position[1] < mouse_down_y < Element.question_position[1]+self.question_width:
                        startscreen.introduceScreen()
                else:
                    self.selected = [-1, -1]

        if button.type == MOUSEBUTTONUP:
            pass

    def exchange(self, spritegroup):
        """点击后交换"""
        if self.exchange_sign == -1:      # 未交换
            self.last_sel = self.selected
        if self.exchange_sign == 1:
            last_x, last_y = Manager.rc_xy(self.last_sel[0], self.last_sel[1])
            sel_x, sel_y = Manager.rc_xy(self.selected[0], self.selected[1])
            if self.last_sel[0] == self.selected[0]:  # 左右相邻
                for animallist in spritegroup:
                    if animallist.rect.topleft == (last_x, last_y):
                        last_sprite = animallist
                        last_sprite.speed = [self.selected[1]-self.last_sel[1], 0]
                    elif animallist.rect.topleft == (sel_x, sel_y):
                        selected_sprite = animallist
                        selected_sprite.speed = [self.last_sel[1]-self.selected[1], 0]
            else:   # 上下相邻
                for animallist in spritegroup:
                    if animallist.rect.topleft == (last_x, last_y):
                        last_sprite = animallist
                        last_sprite.speed = [0, self.selected[0]-self.last_sel[0]]
                    elif animallist.rect.topleft == (sel_x, sel_y):
                        selected_sprite = animallist
                        selected_sprite.speed = [0, self.last_sel[0]-self.selected[0]]
            while last_sprite.speed != [0, 0]:
                pygame.time.delay(5)
                self.draw_brick(last_x, last_y)
                self.draw_brick(sel_x, sel_y)
                last_sprite.move(last_sprite.speed)
                selected_sprite.move(selected_sprite.speed)
                self.screen.blit(last_sprite.image, last_sprite.rect)
                self.screen.blit(selected_sprite.image, selected_sprite.rect)
                pygame.display.flip()

            self.change_value()
            if self.eliminate_animal():
                self.step -= 1
            else:
                self.change_value()
            self.change_value_sign = False
            self.boom_sel = self.selected
            self.exchange_sign = -1
            self.selected = [-1, -1]

    def change_value(self):
        """交换值"""
        temp = self.animal[self.last_sel[0]][self.last_sel[1]]
        self.animal[self.last_sel[0]][self.last_sel[1]] = self.animal[self.selected[0]][self.selected[1]]
        self.animal[self.selected[0]][self.selected[1]] = temp

    def load_text(self, text, position, txt_size, txt_color=(255, 255, 255)):
        my_font = pygame.font.SysFont(None, txt_size)
        text_screen = my_font.render(text, True, txt_color)
        self.screen.blit(text_screen, position)

    def death_map(self):
        """判断死图，更新图"""
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] != -1:
                    if self.animal[i][j] == self.animal[i][j+1]:
                        if (self.animal[i][j] in [self.animal[i-1][j-1], self.animal[i+1][j-1]] \
                                    and self.animal[i][j-1] != -1) or \
                                (self.animal[i][j] in [self.animal[i-1][j+2], self.animal[i+1][j+2]] \
                                         and self.animal[i][j+2] != -1):
                            self.death_sign = False
                            break
                    if self.animal[i][j] == self.animal[i+1][j]:
                        if (self.animal[i][j] in [self.animal[i-1][j-1], self.animal[i-1][j+1]] \
                                    and self.animal[i-1][j] != -1) or \
                                (self.animal[i][j] in [self.animal[i+2][j - 1], self.animal[i+2][j + 1]] \
                                         and self.animal[i+2][j] != -1):
                            self.death_sign = False
                            break
                    else:
                        if self.animal[i-1][j-1] == self.animal[i][j]:
                            if (self.animal[i][j] == self.animal[i-1][j+1] and self.animal[i-1][j] != -1)\
                                    or (self.animal[i][j] == self.animal[i+1][j-1] and self.animal[i][j-1] != -1):
                                self.death_sign = False
                                break
                        if self.animal[i][j] == self.animal[i+1][j+1]:
                            if (self.animal[i][j] == self.animal[i-1][j+1] and self.animal[i][j+1] != -1)\
                                    or (self.animal[i][j] == self.animal[i+1][j-1] and self.animal[i+1][j] != -1):
                                self.death_sign = False
                                break
        if self.death_sign:
            pygame.time.delay(500)
            Element(Element.none_animal, (230, 100)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(800)
            temp = [self.step, self.score, self.animal_num, self.ice_num]
            self.reset_mode = True
            if self.level<6:
              self.set_level_mode(self.level)
            else:
              self.set_level_mode_x(self.level) 
            self.step = temp[0]
            self.score = temp[1]
            self.animal_num = temp[2]
            self.ice_num = temp[3]
        else:
            self.death_sign = True

  
    def exist_left(self, i, j, num):
        sl = 0
        for temp in range(0,int(num)):
            if self.animal[i][j] == self.animal[i][j-temp] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                sl += 1
                if sl == num:
                    return True
            else:
                return False

    def exist_right(self, i, j, num):
        sr = 0
        for temp in range(0, int(num)):
            if self.animal[i][j] == self.animal[i][j + temp] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                sr = sr + 1
                if sr == num:
                    return True
            else:
                return False

    def exist_up(self, i, j, num):
        su = 0
        for temp in range(0, int(num)):
            if self.animal[i][j] == self.animal[i - temp][j] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                su = su + 1
                if su == num:
                    return True
            else:
                return False

    def exist_down(self, i, j, num):
        sd = 0
        for temp in range(0, int(num)):
            if self.animal[i][j] == self.animal[i + temp][j] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                sd = sd + 1
        
                if sd == num:
                    return True
                else:pass
            else:
                return False

    def change_left(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        for k in range(0,int(num)):
            self.animal[i][j-k] = -2
    
    def change_right(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        for k in range(0,int(num)):
            self.animal[i][j+k] = -2
      

    def change_up(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        for k in range(0,int(num)):
            self.animal[i-k][j] = -2
       

    def change_down(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        for k in range(0,int(num)):
            self.animal[i+k][j] = -2
       

    def eliminate_animal(self):
        score_level = self.score
        self.change_value_sign = False
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                if self.exist_right(i, j, 5):
                    self.change_value_sign = True
                    if self.exist_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  
                        self.change_right(i, j, 5)
                        self.change_down(i, j+2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_right(i, j, 5)
                elif self.exist_right(i, j, 4):
                    self.change_value_sign = True
                    if self.exist_down(i, j+1, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  
                        self.change_right(i, j, 4)
                        self.change_down(i, j+1, 3)
                    elif self.exist_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  
                        self.change_right(i, j, 4)
                        self.change_down(i, j+2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 4
                        SoundPlay(SoundPlay.eliminate[1])  
                        self.change_right(i, j, 4)
                elif self.exist_right(i, j, 3):
                    self.change_value_sign = True
                    if self.exist_down(i, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])
                        self.change_right(i, j, 3)
                        self.change_down(i, j, 3)
                    elif self.exist_down(i, j+1, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_right(i, j, 3)
                        self.change_down(i, j+1, 3)
                    elif self.exist_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_right(i, j, 3)
                        self.change_down(i, j + 2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 3
                        SoundPlay(SoundPlay.eliminate[0])  
                        self.change_right(i, j, 3)
                elif self.exist_down(i, j, 5):
                    self.change_value_sign = True
                    if self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  
                        self.change_down(i, j, 5)
                        self.change_right(i+2, j, 3)
                    elif self.exist_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4]) 
                        self.change_down(i, j, 5)
                        self.change_left(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_down(i, j, 5)
                elif self.exist_down(i, j, 4):
                    self.change_value_sign = True
                    if self.exist_left(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3]) 
                        self.change_down(i, j, 4)
                        self.change_left(i+1, j, 3)
                    elif self.exist_right(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  
                        self.change_down(i, j, 4)
                        self.change_right(i+1, j, 3)
                    elif self.exist_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3]) 
                        self.change_down(i, j, 4)
                        self.change_left(i+2, j, 3)
                    elif self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  
                        self.change_down(i, j, 4)
                        self.change_right(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 4
                        SoundPlay(SoundPlay.eliminate[1])  
                        self.change_down(i, j, 4)
                elif self.exist_down(i, j, 3):
                    self.change_value_sign = True
                    if self.exist_left(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_down(i, j, 3)
                        self.change_left(i+1, j, 3)
                    elif self.exist_right(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2]) 
                        self.change_down(i, j, 3)
                        self.change_right(i+1, j, 3)
                    elif self.exist_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                    elif self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  
                        self.change_down(i, j, 3)
                        self.change_right(i+2, j, 3)
              
                    elif self.exist_left(i+2, j, 2) and self.exist_right(i+2, j, 2):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 2)
                        self.change_right(i+2, j, 2)
                    elif self.exist_left(i+2, j, 2) and self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 2)
                        self.change_right(i+2, j, 3)
                    elif self.exist_left(i+2, j, 3) and self.exist_right(i+2, j, 2):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3]) 
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                        self.change_right(i+2, j, 2)
                    elif self.exist_left(i+2, j, 3) and self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                        self.change_right(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 3
                        SoundPlay(SoundPlay.eliminate[0]) 
                        self.change_down(i, j, 3)

        self.fall_animal()
        if self.score%100 <20 and score_level%100>80:
            self.energy_num+=1
        score_level = self.score - score_level  # 一次点击交换后消除的得分值
        # 根据得分差值，播放不同声音，画不同图片，good，great，amazing，excellent，unbelievable，
        if score_level < 4:
            pass
        elif score_level < 6:           
            SoundPlay(SoundPlay.score_level[0])
            Element(Element.score_level[0], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(700)
        elif score_level < 8:         
            SoundPlay(SoundPlay.score_level[1])
            Element(Element.score_level[1], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(700)
        elif score_level < 9:         
            SoundPlay(SoundPlay.score_level[2])
            Element(Element.score_level[2], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(700)
        elif score_level < 10:          
            SoundPlay(SoundPlay.score_level[3])
            Element(Element.score_level[3], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(700)
        elif score_level >= 10:        
            SoundPlay(SoundPlay.score_level[4])
            Element(Element.score_level[4], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(700)

        return self.change_value_sign
    
 
    def fall_animal(self):
        """下落函数"""
        clock = pygame.time.Clock()
        position = []
        ice_position = []
        for i in range(self.row, self.row+self.height):
            for j in range(self.col, self.col+self.width):
                if self.animal[i][j] == -2:
                    x, y = self.rc_xy(i, j)
                    position.append((x, y))
                    if self.ice_list[i][j] == 1:
                        ice_position.append((x, y))
        if position != []:
            for index in range(0, 9):
                clock.tick(20)
                for pos in position:
                    self.draw_brick(pos[0], pos[1])
                    if pos in ice_position:
                        Element(Element.ice_eli[index], (pos[0], pos[1])).draw(self.screen)
                    Element(Element.bling[index], (pos[0], pos[1])).draw(self.screen)
                    pygame.display.flip()
       
        for i in range(self.row, self.row + self.height):
            brick_position = []
            fall_animal_list = []
            speed = [0, 1]
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] == -2:

                    x, y = self.rc_xy(i, j)
                    if self.ice_list[i][j] == 1:
                        SoundPlay(SoundPlay.ice_break)
                        self.ice_num += 1
                        self.ice_list[i][j] = -1
                        
                    brick_position.append((x, y))

                    for m in range(i,  - 1, -1):
                        if self.animal[m - 1][j] != -1:
                            x, y = self.rc_xy(m - 1, j)
                            brick_position.append((x, y))
                            animal = Element(Element.animal[self.animal[m - 1][j]], (x, y))
                            fall_animal_list.append(animal)
                            self.animal[m][j] = self.animal[m - 1][j]
                        else:
                            self.animal[m][j] = random.randint(0, 5)
                            break
            while speed != [0, 0] and fall_animal_list != []:
                for position in brick_position:
                    self.draw_brick(position[0], position[1])
                for animal_sprite in fall_animal_list:
                    animal_sprite.move(speed)
                    animal_sprite.draw(self.screen)
                    speed = animal_sprite.speed
                pygame.display.flip()



    def judgeNext(self, type, score):
        """判断下一步是过关还是失败"""
        if type == 1:      # 过关
            self.loadFnsWindow(score)
        elif type == -1:   # 过关失败
            self.loadFailWindow()

    def loadFailWindow(self):
        """画失败板子及相关按钮"""
        sound_sign = 0
        retry = Board(Board.replay, Board.button_position[1])               # 右再来一次按钮
        step_add = Board(Board.step_add, Board.button_position[0])          # 左再来5步按钮
        self.screen.blit(self.fail_board.image, self.fail_board.rect)   # 过关失败板
        self.screen.blit(step_add.image, step_add.rect)
        self.screen.blit(retry.image, retry.rect)
        while self.fail_board.speed != [0, 0]:
            self.draw()
            self.screen.blit(self.fail_board.image, self.fail_board.rect)
            self.fail_board.move()
            pygame.display.flip()
            if sound_sign == 0:
                SoundPlay(SoundPlay.board_sound)
                sound_sign = 1

    def loadFnsWindow(self, score):
        """过关成功及相关按钮"""
        sound_sign = 0
        next_level = Board(Board.next, Board.button_position[1])              # 右下一关按钮
        replay = Board(Board.replay, Board.button_position[0])                # 左再来一次按钮
        self.screen.blit(self.success_board.image, self.success_board.rect)     # 过关成功板
        self.screen.blit(next_level.image, next_level.rect)
        self.screen.blit(replay.image, replay.rect)
        while self.success_board.speed != [0, 0]:
            self.draw()
            self.screen.blit(self.success_board.image, self.success_board.rect)
            self.success_board.move()
            pygame.display.flip()
            if sound_sign == 0:
                SoundPlay(SoundPlay.board_sound)
                sound_sign = 1
        self.displayStars(score)                 # 画星星
        # 画银币
        self.load_text(str(self.score*2), (Board.starts_position[0][0]+60, Board.starts_position[0][0]+30), 25, (0, 0, 0))

    def displayStars(self, score):
        """画星星"""
        star1 = Board(Board.stars, Board.starts_position[0])
        star2 = Board(Board.stars, Board.starts_position[1])
        star3 = Board(Board.stars, Board.starts_position[2])
        if 0 <= score < self.min*2:
            self.load_text(str(" "), (Board.starts_position[1][0]+48, Board.starts_position[1][1]+35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
        elif self.min*2 <= score <= self.max*2:
            self.load_text(str(" "), (Board.starts_position[1][0] + 48, Board.starts_position[1][1] + 35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
            self.screen.blit(star2.image, star2.rect)
        elif score > self.max*2:
            self.load_text(str(" "), (Board.starts_position[1][0] + 48, Board.starts_position[1][1] + 35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
            self.screen.blit(star2.image, star2.rect)
            self.screen.blit(star3.image, star3.rect)
        pygame.display.flip()

    def set_level_mode(self, level):
    
        self.level = level
        if self.reset_mode:            
            self.num_sign = True
            if level == 1:
                self.__init__(7, 7)
                self.animal[7][9] = self.animal[7][10] = self.animal[7][11] = self.animal[8][10] = self.animal[11][7] = \
                    self.animal[11][13] = self.animal[12][7] = self.animal[12][8] = self.animal[12][12] = self.animal[12][13] = \
                    self.animal[13][7] = self.animal[13][8] = self.animal[13][9] = self.animal[13][11] = self.animal[13][12] = \
                    self.animal[13][13] = -1
                self.init_step = 17          
            elif level == 2:
                self.__init__(4, 8)
                self.init_step = 16         
            elif level == 3:
                self.__init__(7, 7)
                self.init_step = 18      
            elif level == 4:
                self.__init__(9, 7)
                row, col = self.row, self.col
                self.animal[row][col] = self.animal[row][col+7] = self.animal[row][col+8] = self.animal[row+1][col+8] = \
                    self.animal[row+5][col] = self.animal[row+6][col] = self.animal[row+6][col+1] = self.animal[row+6][col+8] = -1
                self.init_step = 20
            elif level == 5:
                self.__init__(8, 9)
                row, col = self.row, self.col
                self.animal[row][col+7] = self.animal[row+2][col] = self.animal[row+5][col] = self.animal[row+3][col+7] = \
                    self.animal[row+6][col+7] = self.animal[row+8][col] = -1
                self.init_step = 20
            elif level == 6:
                self.__init__(7, 8)
                row, col = self.row, self.col
                for i in range(row+2, row+5):
                    for j in range(col+1, col+6):
                        self.ice_list[i][j] = 1
                self.init_step = 21
            elif level == 7:
                self.__init__(9, 9)
                row, col = self.row, self.col
                self.animal[row][col+4] = self.animal[row+4][col] = self.animal[row+4][col+8] = self.animal[row+8][col+4] = -1
                for i in range(row+1, row+8):
                    for j in range(col+1, col+8):
                        self.ice_list[i][j] = 1
                self.init_step = 35
            else:
                self.__init__(9, 9)
                row, col = self.row, self.col
                for i in range(row, row+2):
                    for j in range(col, col+9):
                        self.animal[i][j] = -1
                self.animal[row][col+4] = random.randint(0, 5)
                self.animal[row+1][col+2] = random.randint(0, 5)
                self.animal[row+1][col+4] = random.randint(0, 5)
                self.animal[row+1][col+6] = random.randint(0, 5)
                self.animal[row+2][col+1] = self.animal[row+3][col+1] = self.animal[row+2][col+3] = self.animal[row+3][col+3] =\
                    self.animal[row+2][col+5] = self.animal[row+3][col+5] = self.animal[row+2][col+7] = \
                    self.animal[row+3][col+7] = self.animal[row+8][col] = self.animal[row+8][col+8] = -1
                for i in range(row+4, row+8):
                    for j in range(col, col+9):
                        self.ice_list[i][j] = 1
                self.ice_list[row+2][col+4] = self.ice_list[row+3][col+2] = self.ice_list[row+3][col+4] = \
                    self.ice_list[row+3][col+6] = 1
                self.init_step = 40
            self.type = 0
            self.success_board = Board(Board.success_board, [200, 0])  # 过关成功板
            self.fail_board = Board(Board.fail_board, [200, 0])  # 任务失败板
            self.step = self.init_step
            self.score = 0
            self.animal_num = [0, 0, 0, 0, 0, 0]
            self.ice_num = 0
            self.energy_num = 0
            self.reset_mode = False
            
    def set_level_mode_x(self,level):       
            if level == 6:
                row, col = self.row, self.col
                self.reset_animal()
                for i in range(row+2, row+5):
                    for j in range(col+1, col+6):
                      if self.ice_list[i][j] != -1:  
                        self.ice_list[i][j] = 1
                self.init_step = 21
            elif level == 7:
                row, col = self.row, self.col
                self.reset_animal()
                self.animal[row][col+4] = self.animal[row+4][col] = self.animal[row+4][col+8] = self.animal[row+8][col+4] = -1
                for i in range(row+1, row+8):
                    for j in range(col+1, col+8):
                      if self.ice_list[i][j] != -1:
                        self.ice_list[i][j] = 1
                self.init_step = 35
            else:
                row, col = self.row, self.col
                self.reset_animal()
                for i in range(row, row+2):
                    for j in range(col, col+9):
                        self.animal[i][j] = -1
                self.animal[row][col+4] = random.randint(0, 5)
                self.animal[row+1][col+2] = random.randint(0, 5)
                self.animal[row+1][col+4] = random.randint(0, 5)
                self.animal[row+1][col+6] = random.randint(0, 5)
                self.animal[row+2][col+1] = self.animal[row+3][col+1] = self.animal[row+2][col+3] = self.animal[row+3][col+3] =\
                    self.animal[row+2][col+5] = self.animal[row+3][col+5] = self.animal[row+2][col+7] = \
                    self.animal[row+3][col+7] = self.animal[row+8][col] = self.animal[row+8][col+8] = -1
                for i in range(row+4, row+8):
                    for j in range(col, col+9):
                      if self.ice_list[i][j] != -1:
                        self.ice_list[i][j] = 1
                if self.ice_list[row+2][col+4] != -1:
                    self.ice_list[row+2][col+4] = 1
                if self.ice_list[row+3][col+2] != -1:
                    self.ice_list[row+3][col+2] = 1
                if self.ice_list[row+3][col+4] != -1:
                    self.ice_list[row+3][col+4] = 1
                if self.ice_list[row+3][col+6] != -1:
                     self.ice_list[row+3][col+6] = 1
                self.init_step = 40
            self.type = 0
            self.success_board = Board(Board.success_board, [200, 0])  # 过关成功板
            self.fail_board = Board(Board.fail_board, [200, 0])  # 任务失败板
            self.step = self.init_step
            self.score = 0
            self.animal_num = [0, 0, 0, 0, 0, 0]
            self.ice_num = 0
            self.reset_mode = False
            
            
    def num_add(self):
        if self.num_sign:
            self.money += self.score * 2
            self.num_sign = False

    def judge_level(self):
        """每关任务判断过关"""
        if self.step <= 0:
            self.type = -1  
        if self.level == 1:
            if self.animal_num[self.animals[0]] >= 10:  
                self.type = 1             
                self.num_add()
        elif self.level == 2:
            if self.animal_num[self.animals[1]] >= 21:  
                self.type = 1                        
                self.num_add()
        elif self.level == 3:
            if self.animal_num[self.animals[2]] >= 16 and self.animal_num[self.animals[3]] >= 16:  
                self.type = 1                        
                self.num_add()
        elif self.level == 4:
            if self.animal_num[self.animals[4]] >= 18 and self.animal_num[self.animals[5]] >= 18:
                self.type = 1                       
                self.num_add()

        elif self.level == 5:
            if self.animal_num[self.animals[self.choose[0]]] >= 28 and self.animal_num[self.animals[self.choose[1]]] >= 28:  
                self.type = 1                         
                self.num_add()

        elif self.level == 6:
            if self.ice_num >= 15:  
                self.type = 1                         # 过关
                self.num_add()

        elif self.level == 7:
            if self.ice_num >= 49:  
                self.type = 1                         # 过关
                self.num_add()

        else :
            if self.ice_num >= 40:
                self.type = 1                         
                self.num_add()

        self.judgeNext(self.type, self.score)
