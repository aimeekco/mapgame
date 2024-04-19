import pygame
from pygame.locals import *
from maze import *

class Food:
    def __init__(self):
        self.img = pygame.image.load('food.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def eat_food():
    global score
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            score += 1
            return True
    return False


def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        time, score, FPS = 60, 0, 60


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# get maze
maze = generate_maze()

# player settings
player_speed = 5
player_img = pygame.image.load('0.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'left': (-player_speed, 0), 'right': (player_speed, 0), 'up': (0, -player_speed), 'down': (0, player_speed)}
keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}
direction = (0, 0)

# food settings
food_list = [Food() for i in range(3)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)


while True:
    game_surface.fill((0,0,0))
    surface.fill(pygame.Color('black'), (WIDTH, 0, 300, HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1
            if time <= 0:
                is_game_over()
            
    for cell in maze:
        cell.draw(game_surface)

    # controls and movement
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # draw maze
    # [cell.draw(game_surface) for cell in maze]
    generate_maze()

    # gameplay
    if eat_food():
        FPS += 10
        score += 1
    is_game_over()

    # draw player
    game_surface.blit(player_img, player_rect)

    # draw food
    [food.draw() for food in food_list]

    # draw stats
    time_text = text_font.render('Time', True, pygame.Color('white'))
    time_value = font.render(f'{time}', True, pygame.Color('white'))
    score_text = text_font.render('Score:', True, pygame.Color('white'))
    score_value = font.render(f'{score}', True, pygame.Color('white'))

    surface.blit(time_text, (WIDTH + 70, 30))
    surface.blit(time_value, (WIDTH + 70, 130))
    surface.blit(score_text, (WIDTH + 50, 350))
    surface.blit(score_value, (WIDTH + 70, 430))

    surface.blit(game_surface, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)