import pygame as pg


class SoundManager:
    
    def __init__(self):
        self.bg_music = pg.mixer.music.load(r"assets/sfx/bg_music.wav")
        self.enemy_collision = pg.mixer.Sound(r"assets/sfx/enemy_collision.wav")
        self.friendly_collision = pg.mixer.Sound(r"assets/sfx/friendly_collision.wav")
        self.reproduce = pg.mixer.Sound(r"assets/sfx/reproduce.wav")
        self.grass_eaten = pg.mixer.Sound(r"assets/sfx/grass_eaten.wav")
    
    def play_bg(self):
        pg.mixer.music.play(-1)
    
    def play_enemy_collision(self):
        self.enemy_collision.play()
    
    def play_friend_collision(self):
        self.friendly_collision.play()
        
    def play_reproduce(self):
        self.reproduce.play()
    
    def play_eat_grass(self):
        self.grass_eaten.play()