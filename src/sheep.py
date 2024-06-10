import pygame as pg

from config import *
from entity import Entity, Types
from neural_network import NeuralNetwork

from random import random

class Sheep(Entity):
    
    def __init__(self, env, sprite_manager, intial_position: v2, nn):
        self.gender = 1 if random() <= SHEEP_MALE_ODDS else 0
        super().__init__(env, intial_position, sprite_manager.male_sheep if self.gender else sprite_manager.female_sheep, nn)
        self.type = Types.SHEEP
        self.speed = FPS
    
    def eat(self, grass_map):
        # Snapped position
        x, y = int(self.rect.topleft[0] // TILE_SIZE), int(self.rect.topleft[1] // TILE_SIZE)
        if self.energy <= EATING_ENERGY_THRESHOLD and grass_map.get_state(x, y) == 1.0:
            self.energy = 100.0
            self.env.sound_manager.play_eat_grass()
            grass_map.eat_at(x, y)
    
    def handle_collision(self, t: Types, g: int):
        if t == Types.WOLF:
            self.is_alive = False
        else:
            self.env.sound_manager.play_friend_collision()
            if self.gender != g and self.energy >= (SHEEP_REPRODUCTION_REQUIREMENT * MAX_ENERGY):
                self.env.sound_manager.play_reproduce()
                if self.gender == 0:  # Spawn from females
                    self.child_number += 1
                    child = Sheep(self.env, 
                                self.env.sprite_manager, 
                                v2(random() * WIDTH, random() * HEIGHT),
                                NeuralNetwork())
                    child.energy = CHILD_ENERGY
                    self.env.sheep_history.append(self.env.sheeps[-1])
    
    def respawn(self):
        self.is_alive = True
        self.energy = MAX_ENERGY
        self.survival_time = 0.0
        self.child_number = 0  
        self.gender = 1 if random() <= SHEEP_MALE_ODDS else 0
        self.sprite = self.env.sprite_manager.male_sheep if self.gender else self.env.sprite_manager.female_sheep
        
    def process(self, dt: float):
        self.move(dt)
        self.expend_energy(dt)
        self.animate(dt)