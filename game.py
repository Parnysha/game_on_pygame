import pygame
import random
import time
pygame.init()

pygame.font.init()
score_font = pygame.font.SysFont('Arial',40)
menu_font = pygame.font.SysFont('Arial',100)


start_time = time.time()
obj_start_time=time.time()
DISPLAY_HEIGHT = 480
DISPLAY_WIDTH = 640

STATE_START = 0
STATE_GAME = 1
STATE_GAMEOVER = 2
current_state = STATE_START

class GameObject():
    def __init__(self,hp,x,y,height, width,damage,color,image_name = ''):
        self.hp = hp
        self.rect = pygame.Rect(0,0,width,height)
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y
        self.color = color
        self.damage = damage
        if image_name != '':
            self.image = pygame.image.load(image_name)
            self.image.set_colorkey((0,0,0))
        else:
            self.image = None
    def move(self,dx,dy,dt):
        self.x += dx * dt # self.x = self.x +dx
        self.y += dy * dt

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, surface):
        if self.image is not None:
            surface.blit(self.image,self.rect.topleft)
        else:
            pygame.draw.rect(surface,self.color,self.rect)

class Player(GameObject):
    def __init__(self,hp,x,y,height, width,damage,color):
        super().__init__(hp,x,y,height, width,damage,color)
        self.bullet_list = []
        self.bullet_speed = 50
        self.bullet_draw_start = time.time()
        self.score = 0
        self.image = pygame.image.load('bazuka.png')
        self.image.set_colorkey((255,255,255))
    def move(self,x,y):
        dx = x - self.x
        dy = y - self.y

        self.x = self.x + dx * 0.001
        self.y = self.y + dy * 0.001

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def shoot(self):
        player_right_x, player_right_y = self.rect.midright
        bullet = GameObject(1,player_right_x + 3,player_right_y,6,6,1,(255,255,255), 'bullet.png')
        self.bullet_list.append(bullet)

    def draw_bullets(self,surface):
        current_time = time.time()
        dt = current_time - self.bullet_draw_start
        self.bullet_draw_start = current_time
        for i,bullet in enumerate(self.bullet_list):
            bullet.move(self.bullet_speed,0,dt)
            bullet.draw(surface)
            if bullet.x > DISPLAY_WIDTH:
                self.bullet_list.pop(i)

    def hit_npc(self,npc):
        for i,bullet in enumerate(self.bullet_list):
            if npc.rect.colliderect(bullet.rect):
                npc.hp -= bullet.damage
                self.bullet_list.pop(i)
                if npc.hp <= 0:
                    self.score += 1


def draw_start(screen,game_state):
    global menu_font,current_state
    new_game_img = menu_font.render('Начать игру', True, (255, 255, 255))
    exit_game_img = menu_font.render('Выход', True, (255, 255, 255))
    new_game_x = 100
    new_game_y = 80
    exit_game_x = 100
    exit_game_y = 190
    events = pygame.event.get()

    inactive_color = (255,255,255)
    pressed_color = (0,0,0)
    hover_color = (128,128,128)

    new_game_color = inactive_color
    exit_game_color = inactive_color

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                new_game_rect = new_game_img.get_rect()
                new_game_rect.topleft = (new_game_x,new_game_y)
                exit_game_rect = exit_game_img.get_rect()#чтобы считать коорд
                exit_game_rect.topleft = (exit_game_x,exit_game_y)#левая часть прямоугольника выход
                if new_game_rect.collidepoint(event.pos):#если точка курсора пересекается с прямоугольником
                    new_game_color = pressed_color
                    current_state = STATE_GAME
                elif exit_game_rect.collidepoint(event.pos):
                    exit_game_color = pressed_color
                    pygame.quit()

    mouse_pos = pygame.mouse.get_pos()
    new_game_rect = new_game_img.get_rect()
    new_game_rect.topleft = (new_game_x, new_game_y)
    exit_game_rect = exit_game_img.get_rect()  # чтобы считать коорд
    exit_game_rect.topleft = (exit_game_x, exit_game_y)  # левая часть прямоугольника выход
    if new_game_rect.collidepoint(mouse_pos):  # если точка курсора пересекается с прямоугольником
        new_game_color = hover_color
    elif exit_game_rect.collidepoint(mouse_pos):
        exit_game_color = hover_color
    screen.fill((0, 0, 0))
    new_game_img = menu_font.render('Начать игру', True, new_game_color)
    exit_game_img = menu_font.render('Выход', True, exit_game_color)
    screen.blit(new_game_img,(new_game_x,new_game_y))
    screen.blit(exit_game_img,(exit_game_x,exit_game_y))

def draw_game(screen, game_state,player,npc_list):
    global obj_time_start, start_time,current_state
    events = pygame.event.get()
    #обработка событий
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key == pygame.K_f:
                if player.hp > 0:
                    player.shoot()

    current_time = time.time()
    dt = current_time - start_time
    if dt > 0.5: #прошло 0.5 секунды
        x = 640
        y = random.randint(0, 480)
        npc = GameObject(1, x, y, 15, 15, 1, (150, 200, 15),'tank.png')
        npc_list.append(npc)
        start_time = current_time

    screen.fill((0, 0, 0))
    #игровая логика
    mouse_pos = pygame.mouse.get_pos()
    player.move(mouse_pos[0], mouse_pos[1])

    obj_time_current = time.time()
    obj_dt = obj_time_current - obj_time_start
    obj_time_start = obj_time_current
    for i, npc in enumerate(npc_list):
        npc.move(-100, -0, obj_dt)
        npc.draw(screen)
        if npc.x < 0 - npc.rect.width / 2:
            npc_list.pop(i)
        if npc.rect.colliderect(player.rect) and player.hp > 0:
            player.hp = player.hp - npc.damage
            npc_list.pop(i)
        player.hit_npc(npc)
        if npc.hp <= 0:
            npc_list.pop(i)
    if player.hp > 0:
        player.draw(screen)  # отрисовка игрока
        player.draw_bullets(screen)
    else:
        current_state = STATE_GAMEOVER
    score_display = score_font.render(str(player.score), True, (255, 255, 255))
    screen.blit(score_display, (DISPLAY_WIDTH - 100, 5))


def draw_gameover(screen,game_state,player):
    global menu_font, current_state,npc_list
    game_over_img = menu_font.render('Вы проиграли', True, (255, 255, 255))
    new_game_img = menu_font.render('Начать игру', True, (255, 255, 255))
    exit_game_img = menu_font.render('Выход', True, (255, 255, 255))
    new_game_x = 100
    new_game_y = 100
    exit_game_x = 100
    exit_game_y = 200
    events = pygame.event.get()

    inactive_color = (255, 255, 255)
    pressed_color = (0, 0, 0)
    hover_color = (128, 128, 128)

    new_game_color = inactive_color
    exit_game_color = inactive_color

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                new_game_rect = new_game_img.get_rect()
                new_game_rect.topleft = (new_game_x, new_game_y)
                exit_game_rect = exit_game_img.get_rect()  # чтобы считать коорд
                exit_game_rect.topleft = (exit_game_x, exit_game_y)  # левая часть прямоугольника выход
                if new_game_rect.collidepoint(event.pos):  # если точка курсора пересекается с прямоугольником
                    new_game_color = pressed_color
                    npc_list = []
                    player.hp = 5
                    player.score = 0
                    player.bullet_list = []
                    current_state = STATE_GAME
                elif exit_game_rect.collidepoint(event.pos):
                    exit_game_color = pressed_color
                    pygame.quit()

    mouse_pos = pygame.mouse.get_pos()
    new_game_rect = new_game_img.get_rect()
    new_game_rect.topleft = (new_game_x, new_game_y)
    exit_game_rect = exit_game_img.get_rect()  # чтобы считать коорд
    exit_game_rect.topleft = (exit_game_x, exit_game_y)  # левая часть прямоугольника выход
    if new_game_rect.collidepoint(mouse_pos):  # если точка курсора пересекается с прямоугольником
        new_game_color = hover_color
    elif exit_game_rect.collidepoint(mouse_pos):
        exit_game_color = hover_color
    screen.fill((0, 0, 0))
    new_game_img = menu_font.render('Начать игру', True, new_game_color)
    exit_game_img = menu_font.render('Выход', True, exit_game_color)
    screen.blit(game_over_img,(100,0))
    screen.blit(new_game_img, (new_game_x, new_game_y))
    screen.blit(exit_game_img, (exit_game_x, exit_game_y))


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

game_state = STATE_START


player = Player(5,200,200,20,40,1,(0,0,255))
npc_list = []
obj_time_start = start_time = time.time()

while True:
    if current_state == STATE_START:
        draw_start(screen,current_state)
    elif current_state == STATE_GAME:
        draw_game(screen, current_state, player, npc_list)
    elif current_state == STATE_GAMEOVER:
        draw_gameover(screen,current_state,player)
