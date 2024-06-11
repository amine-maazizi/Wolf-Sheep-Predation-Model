import pygame as pg
import sys
from random import randint
import random
from time import time

from config import *
from grass_map import GrassMap
from sprite_manager import SpriteManager
from entity import Types
from sheep import Sheep
from wolf import Wolf
from neural_network import NeuralNetwork
from collision_manager import CollisionManager
from sound_manager import SoundManager


class Environment:
    
    def __init__(self):
        # Pygame initialisation
        pg.init()
        pg.display.set_caption(TITLE)
        self.display = pg.display.set_mode([SCALING_FACTOR * WIDTH, SCALING_FACTOR * HEIGHT])
        self.scaling_surf = pg.Surface([WIDTH, HEIGHT])
        
        self.clock = pg.time.Clock()
        self.dt, self.last_time = 0.0, time()
        
        self.sprite_manager = SpriteManager()
        self.sound_manager = SoundManager()
        self.sound_manager.play_bg()
        
    
    def play_step(self):
        """Runs one step of the simulation"""
        
        for ev in pg.event.get():
            if ev.type == pg.QUIT or (ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
        
        self.render()
        self.process(self.dt)
        
        self.dt, self.last_time = time() - self.last_time, time()
        self.simulation_timer += self.dt * FPS
        
        pg.display.update()
        self.clock.tick(FPS) 
        
        if (len(self.wolfs) == 0 or len(self.sheeps) == 0) or self.simulation_timer >= GENERATION_DURATION:
            self.simulation_over = True
        
        return self.simulation_timer, self.sheep_history, self.wolf_history, len(self.sheeps), len(self.wolfs)
    
    def render(self):
        """Handles the rendering part of the simulation"""
        self.scaling_surf.fill(BG_COLOR)
        self.grass_map.render(self.scaling_surf)
        
        for sheep in self.sheeps:
            sheep.render(self.scaling_surf)
            
        for wolf in self.wolfs:
            wolf.render(self.scaling_surf)
        
        # Scaling procedure
        self.display.blit(
            pg.transform.scale(
                self.scaling_surf, 
                [SCALING_FACTOR * WIDTH, SCALING_FACTOR * HEIGHT]
                ), 
            (0, 0)
            )
    
    def process(self, dt: float):
        """Handles the processing part of the simulation"""
        if self.prediction_timer  >= TIME_BETWEEN_PREDICTION:
            for sheep in self.sheeps:
                sheep.make_prediction() 
            for wolf in self.wolfs:
                wolf.make_prediction()
            self.prediction_timer = 0.0
            
        for sheep in self.sheeps:
            sheep.process(dt)
            sheep.eat(self.grass_map)
            if not sheep.is_alive:
                self.sheeps.remove(sheep)
        for wolf in self.wolfs:
            wolf.process(dt)
            if not wolf.is_alive:
                self.wolfs.remove(wolf)
        self.prediction_timer += 1.0
        
        self.collision_manager.process_collisions(self.update_collisions())
        self.grass_map.grow(dt)
            
    def spawn_entities(self, population=None):
        self.grass_map = GrassMap(self.sprite_manager)
        self.prediction_timer = 0.0
        self.simulation_over = False
        self.simulation_timer = 0.0

        visited_positions = []
        self.sheeps = []
        self.wolfs = []

        if population:
            for entity in population:
                entity.respawn()
                if entity.type == Types.SHEEP:
                    pos = self.get_random_position(visited_positions, top_half=True)
                    self.sheeps.append(entity)
                else:
                    pos = self.get_random_position(visited_positions, top_half=False)
                    self.wolfs.append(entity)
                entity.rect.topleft = pos
                visited_positions.append(pos)
        else:
            for i in range(SHEEP_POPULATION):
                pos = self.get_random_position(visited_positions, top_half=True)
                self.sheeps.append(Sheep(self, self.sprite_manager, pos, NeuralNetwork().to(device)))
                visited_positions.append(pos)
                
            for i in range(WOLF_POPULATION):
                pos = self.get_random_position(visited_positions, top_half=False)
                self.wolfs.append(Wolf(self, self.sprite_manager, pos, NeuralNetwork().to(device)))
                visited_positions.append(pos)

        self.sheep_history = self.sheeps.copy()
        self.wolf_history = self.wolfs.copy()
        self.collision_manager = CollisionManager()

    def get_random_position(self, visited_positions, top_half=True):
        if top_half:
            pos = v2(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT // 2 - 1)) // TILE_SIZE * TILE_SIZE
        else:
            pos = v2(random.randint(0, WIDTH - 1), random.randint(HEIGHT // 2, HEIGHT - 1)) // TILE_SIZE * TILE_SIZE
        while pos in visited_positions:
            if top_half:
                pos = v2(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT // 2 - 1)) // TILE_SIZE * TILE_SIZE
            else:
                pos = v2(random.randint(0, WIDTH - 1), random.randint(HEIGHT // 2, HEIGHT - 1)) // TILE_SIZE * TILE_SIZE
        return pos

    def update_collisions(self):
        self.collisions = {}
        for sheep in self.sheeps:
            self.collisions[sheep] = sheep.rect
        for wolf in self.wolfs:
            self.collisions[wolf] = wolf.rect
        return self.collisions
