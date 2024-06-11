import pygame as pg

from config import *
from entity import Entity, Types
from neural_network import NeuralNetwork

from random import random

class Wolf(Entity):
    
    def __init__(self, env, sprite_manager, intial_position: v2, nn):
        self.gender = 1 if random() <= WOLF_MALE_ODDS else 0
        super().__init__(env, intial_position, sprite_manager.male_wolf if self.gender else sprite_manager.female_wolf, nn)
        self.type = Types.WOLF
        self.speed = 1.0
        self.sheep_eaten = 0
    
    def handle_collision(self, t: Types, g: int):
        if t == Types.SHEEP:
            self.env.sound_manager.play_enemy_collision()
            self.energy = 100.0
            self.sheep_eaten += 1
        else:
            self.env.sound_manager.play_friend_collision()
            if self.gender != g and self.energy >= (WOLF_REPRODUCTION_REQUIREMENT * MAX_ENERGY):
                self.env.sound_manager.play_reproduce()
                if self.gender == 0:  # Spawn from females
                    self.child_number += 1
                    child = Wolf(self.env, 
                                self.env.sprite_manager, 
                                v2(random() * WIDTH, random() * HEIGHT),
                                NeuralNetwork())
                    child.energy = CHILD_ENERGY
                    self.env.wolfs.append(child)
                    self.env.wolf_history.append(self.env.wolfs[-1])
    
    def respawn(self):
        self.is_alive = True
        self.energy = MAX_ENERGY
        self.survival_time = 0.0
        self.child_number = 0  
        self.sheep_eaten = 0
        self.gender = 1 if random() <= WOLF_MALE_ODDS else 0
        self.sprite = self.env.sprite_manager.male_wolf if self.gender else self.env.sprite_manager.female_wolf
    
    
    def process(self, dt: float):
        self.move(dt)
        self.expend_energy(dt)
        self.animate(dt)