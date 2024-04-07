import pygame
from pygame.locals import *
from collections import deque
from random import choice 

RES = WIDTH, HEIGHT = 1202, 902
TILE = 100
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

#USER CHARACTER
x, y = 0,0
velocity = 5
speed_increase = 0.5
max_velocity = 20

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'top': True, 'right':True, 'bottom': True, 'left': True}
    
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('red'), (x+2, y+2, TILE-2, TILE-2))
        
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y + TILE), (x, y), 2)
            
    def has_wall(self, direction):
        return self.walls[direction]
            
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols-1 or y < 0 or y > rows-1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y-1)
        right = self.check_cell(self.x+1, self.y)
        bottom = self.check_cell(self.x, self.y+1)
        left = self.check_cell(self.x-1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False
        
def move_character(x,y,dx,dy,cells):
    new_x = x + dx
    new_y = y + dy
    cell_x, cell_y = int(new_x // TILE), int(new_y // TILE)
    
    if 0 <= cell_x < cols and 0 <= cell_y < rows:
        current_cell = cells[cell_y * cols + cell_x]
    
        if dx > 0 and current_cell.has_wall('right'):
            new_x = cell_x * TILE
        elif dx < 0 and current_cell.has_wall('left'):
            new_x = (cell_x + 1) * TILE
        if dy > 0 and current_cell.has_wall('bottom'):
            new_y = cell_y * TILE
        elif dy < 0 and current_cell.has_wall('top'):
            new_y = (cell_y + 1) * TILE
        
    else:
        new_x, new_y = x, y
    
    return new_x, new_y

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
colors, color = [], 40


running = True
keys_held = {K_LEFT: False, K_RIGHT: False, K_UP: False, K_DOWN: False}

while True:
    sc.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            runnning = False
        elif event.type == KEYDOWN:
            keys_held[event.key] = True
        elif event.type == KEYUP:
            keys_held[event.key] = False
            velocity = 5

    if any(keys_held.values()):
        velocity = min(velocity + speed_increase, max_velocity)
    else:
        velocity = 5
        
    dx, dy = 0,0
    if keys_held[K_LEFT]:
        dx = -velocity
    elif keys_held[K_RIGHT]:
        dx = velocity  
    if keys_held[K_UP]:
        dy = -velocity
    elif keys_held[K_DOWN]:
        dy = velocity
        
    x, y = move_character(x, y, dx, dy, grid_cells)

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    [pygame.draw.rect(sc, colors[i], (cell.x * TILE+5, cell.y * TILE+5, TILE-10, TILE-10), border_radius=12) for i, cell in enumerate(stack)]
    
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
        
    pygame.draw.rect(sc, pygame.Color('green'), (x, y, TILE, TILE))
    
    pygame.display.flip()
    clock.tick(30)

