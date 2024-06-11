import pygame as pg
from abc import ABC, abstractmethod
from enum import Enum
from random import randrange, gauss
import math

from config import *

class Types(Enum):
    SHEEP: int = 0
    WOLF: int = 1


class Entity(ABC):
    
    def __init__(self, environment, intial_position: v2, sprite: pg.Surface, nn):
        # Environment reference in order to instanciate entity children in the world 
        # and gain access to neighboring entities
        self.env = environment
        
        
        # Visual and physics related attributes
        self.sprite = sprite
        self.original_sprite = sprite
        self.rect = self.sprite.get_rect()
        
        # Snapping spawn position to grid
        self.rect.topleft = intial_position
        
        self.type = None
        
        # Kinematic variables
        self.speed: int =  1
        self.direction = normalize(v2(randrange(-1, 1), randrange(-1, 1)))
        self.velocity: v2 = v2(0, 0)

        
        # expected and output of 2 representing the direction
        self.nn = nn
        
        # Common simulation attributes
        self.is_alive = True
        self.survival_time: float = 0.0
        self.child_number: int = 0
        self.energy: float = MAX_ENERGY
        self.enery_expenditure = ENERGY_EXPENDITURE_RATE # change this
        
        # Animation related variables
        self.idle_animation_speed = 5
        self.walk_animation_speed = 10
        self.idle_squish_amount = 0.15
        self.walk_rotation_amount = 5
        self.animation_timer = 0
        self.idle = True
    
    def render(self, display):
        if self.sprite:
            display.blit(self.sprite, self.rect)

    def make_prediction(self):
        n_wolf, n_sheep = 0, 0
        for entity in self.env.wolfs + self.env.sheeps:
            if entity == self:
                continue
            x, y = self.rect.topleft
            x_, y_ = entity.rect.topleft
            distance_to_entity = math.sqrt((x-x_)**2 + (y-y_)**2)
            if distance_to_entity <= SEARCH_RADIUS:
                if entity.type == Types.WOLF:
                    n_wolf += 1
                else:
                    n_sheep += 1
                  
        prediciton = self.nn(torch.tensor([n_wolf, n_sheep, self.direction.x, self.direction.y]))
        self.direction = normalize(v2(prediciton[0], prediciton[1]))
    
    def move(self, dt: float):
        # handle border collision
        conditions = [
            (self.rect.x + self.velocity.x) > (WIDTH - TILE_SIZE),
            (self.rect.x + self.velocity.x) < 0,
            (self.rect.y + self.velocity.y) > (HEIGHT - TILE_SIZE),
            (self.rect.y + self.velocity.y) < 0,
        ]
        
        if any(conditions):
            self.direction = - self.direction
        
        # Snap back positions to avoid instability given higher speeds
        if conditions[0]:
            self.rect.right = WIDTH 
        elif conditions[1]:
            self.rect.left = 0
        elif conditions[2]:
            self.rect.bottom = HEIGHT
        elif conditions[3]:
            self.rect.top = 0
            
        self.idle = (self.direction == v2_0)
        
        self.velocity = self.direction * self.speed 

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
    def expend_energy(self, dt: float):
        self.energy = max(0.0, self.energy - (dt * ENERGY_EXPENDITURE_RATE))
        self.survival_time += (dt * FPS)
        
        if self.energy == 0.0:
            self.is_alive = False
        
    def animate(self, dt: float):
        self.animation_timer += dt
        
        if self.idle:
            squish_factor = 1 + self.idle_squish_amount * math.sin(self.animation_timer * self.idle_animation_speed)
            new_height = self.original_sprite.get_height() * squish_factor
            self.sprite = pg.transform.scale(self.original_sprite, (self.original_sprite.get_width(), int(new_height)))
        else:
            rotation_angle = self.walk_rotation_amount * math.sin(self.animation_timer * self.walk_animation_speed)
            self.sprite = pg.transform.rotate(self.original_sprite, rotation_angle)
            self.rect = self.sprite.get_rect(center=self.rect.center)
            
    def save(self, path: str):
        # save neural network weights
        self.nn.save(path)
            
    @abstractmethod
    def handle_collision(self, type: Types, gender: int):
        ...
        
    @abstractmethod
    def process(self, dt):
        ...