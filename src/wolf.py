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
        self.speed = FPS
    
    def handle_collision(self, t: Types, g: int):
        if t == Types.SHEEP:
            self.env.sound_manager.play_enemy_collision()
            self.energy = 100.0
        else:
            self.env.sound_manager.play_friend_collision()
            if self.gender != g and self.energy >= (REPRODUCTION_ENERGY_REQUIREMENT * MAX_ENERGY):
                self.env.sound_manager.play_reproduce()
                if self.gender == 0:  # Spawn from females
                    self.child_number += 1
                    self.env.wolfs.append(Wolf(self.env, 
                                                 self.env.sprite_manager, 
                                                 v2(random() * WIDTH, random() * HEIGHT),
                                                 NeuralNetwork())
                    )
                    self.env.wolf_history.append(self.env.wolfs[-1])
    
    def process(self, dt: float):
        self.move(dt)
        self.expend_energy(dt)
        self.animate(dt)