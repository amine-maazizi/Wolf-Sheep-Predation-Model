import pygame as pg

from config import *

class GrassMap:
    
    def __init__(self, sprite_manger):
        self.sprite = sprite_manger.grass
        self.dimenions = (int(WIDTH // TILE_SIZE), int(HEIGHT // TILE_SIZE))
        # This 2D-matrix contains booleans representing if the grass has been eaten or not
        self.grass_state = [
            [1.0 for _ in range(self.dimenions[1])] for _ in range(self.dimenions[0])
        ]
    
    def grow(self, dt: float):
        for x in range(self.dimenions[0]):
            for y in range(self.dimenions[1]):
                if self.grass_state[x][y] < 1.0:
                    self.grass_state[x][y] = min(self.grass_state[x][y] + GRASS_GROWTH_RATE * dt, 1.0)
    
    def render(self, display):
        for x in range(self.dimenions[0]):
            for y in range(self.dimenions[1]):
                percentage: float = self.grass_state[x][y]
                display.blit(self.sprite, (x * TILE_SIZE,  y * TILE_SIZE), (0, (percentage - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    
    def set_state(self, x, y, value):
        self.grass_state[x][y] = value

    def get_state(self, x, y) -> float:
        return self.grass_state[x][y] 
    
    def eat_at(self, x, y):
        # Eats for grass blocks around the sheep in + shape
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < self.dimenions[0] and 0 <= y + dy < self.dimenions[1]:
                    self.grass_state[x + dx][y + dy] = 0.0
        