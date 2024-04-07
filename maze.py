import pygame
from pygame.locals import *
from collections import deque


def bfs(graph, start, search_value):
    visited = set()
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        if vertex == search_value:
            return True
        visited.add(vertex)
    
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                queue.append(neighbour)
                visited.add(neighbour)
    return False

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

start = "F"
search_value = "B"
res = bfs(graph, start, search_value)
print(f"element {search_value} : {res}")

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BFS Visualization")

x, y = screen_width // 2, screen_height // 2
char_width, char_height = 20, 20
velocity = 5

running = True
while running:
    screen.fill((0, 0, 0)) 
    pygame.draw.rect(screen, (255, 0, 0), (x, y, char_width, char_height))  # Draw the character

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                x -= velocity
            elif event.key == K_RIGHT:
                x += velocity
            elif event.key == K_UP:
                y -= velocity
            elif event.key == K_DOWN:
                y += velocity

    pygame.display.update()
    
pygame.quit()
