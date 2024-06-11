import pygame as pg
import torch

# Pygame constants
WIDTH: int = 322
HEIGHT: int = 322
TILE_SIZE: int = 16
TITLE: str = "Wolf-Sheep predation model"
FPS: int = 60 
SCALING_FACTOR: int = 2

# Type alias
v2 = pg.math.Vector2
v2_0 = v2(0, 0)
v2_1 = v2(1, 1)

# Environment settings
BG_COLOR = [6, 190, 48] 
TIME_BETWEEN_PREDICTION: float = 50.0
ENERGY_EXPENDITURE_RATE: float = 15.0
MAX_ENERGY: float = 100.0
CHILD_ENERGY: float = MAX_ENERGY / 2
GRASS_GROWTH_RATE: float = 0.3
EATING_ENERGY_THRESHOLD: float = 0.2
SHEEP_REPRODUCTION_REQUIREMENT: float = 0.6
WOLF_REPRODUCTION_REQUIREMENT: float = 0.6
SHEEP_MALE_ODDS: float = 0.5
WOLF_MALE_ODDS: float = 0.5

# Evolutionary algorithm settings
SHEEP_POPULATION: int = 20
WOLF_POPULATION: int = 10
SEARCH_RADIUS: float = WIDTH
REPRODUCTION_REWARD: float = 150.0
PREDATORY_REWARD: float = 100.0
# ENERGY_REWARD: float = 20.0
SURVIVAL_REWARD: float = 30.0
WANTED_SURVIVAL_TIME: float = 300.0
SELECTED_ENTITY: int = min(WOLF_POPULATION, SHEEP_POPULATION) // 2
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
MUTATION_SCALE = 0.1
NUM_GENERATIONS = 100
GENERATION_DURATION = 10000

# In the Environment.spawn_entities(), if the below condition is not met it leads to an infinit loop !
assert(SHEEP_POPULATION + WOLF_POPULATION <= (WIDTH // TILE_SIZE * HEIGHT // TILE_SIZE))
assert(SEARCH_RADIUS <= WIDTH and SEARCH_RADIUS <= HEIGHT)
assert(NUM_GENERATIONS > 0)
assert(SELECTED_ENTITY <= SHEEP_POPULATION and SELECTED_ENTITY <= WOLF_POPULATION)


# Neural Network settings
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"NeuralNetwork::Using {device} device")


# Helper functions
def normalize(v: v2):
    if (v != v2_0):
        return v / v.length()
    return v2_0

def lerp(x: float, y: float, f: float) -> float:
    return f * x + (1 - f) * y