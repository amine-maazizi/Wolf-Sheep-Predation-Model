import pygame as pg


class SpriteManager:
    
    def __init__(self) -> None:
        self.male_sheep = pg.image.load("assets/sprites/male_sheep.png")
        self.female_sheep = pg.image.load("assets/sprites/female_sheep.png")
        self.male_wolf = pg.image.load("assets/sprites/male_wolf.png")
        self.female_wolf = pg.image.load("assets/sprites/female_wolf.png")
        self.grass = pg.image.load("assets/sprites/grass.png")
