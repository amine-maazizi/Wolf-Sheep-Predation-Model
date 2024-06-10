from random import choice, random
import numpy as np
import sys

from config import *
from entity import Entity, Types
from sheep import Sheep
from wolf import Wolf
from enivroment import Environment
from neural_network import NeuralNetwork
from training_data import *


def fitness_function(e: Entity):
    predatory_bonus = e.sheep_eaten if e.type == Types.WOLF else 0.0
    return e.child_number * REPRODUCTION_REWARD + predatory_bonus * PREDATORY_REWARD + (e.survival_time / GENERATION_DURATION) * SURVIVAL_REWARD

def select_parents(population, num_parents):
    population.sort(key=fitness_function, reverse=True)
    return population[:num_parents]

def crossover_sheep(parent_1, parent_2):
    child_params = {}
    for param in parent_1.nn.get_params().keys():
        child_params[param] = parent_1.nn.get_params()[param] if random() > 0.5 else parent_2.nn.get_params()[param]
    return Sheep(parent_1.env, parent_1.env.sprite_manager, v2_0, NeuralNetwork(params=child_params))

def crossover_wolf(parent_1, parent_2):
    child_params = {}
    for param in parent_1.nn.get_params().keys():
        child_params[param] = parent_1.nn.get_params()[param] if random() > 0.5 else parent_2.nn.get_params()[param]
    return Wolf(parent_1.env, parent_1.env.sprite_manager, v2_0, NeuralNetwork(params=child_params))

def mutate_sheep(sheep):

    for param in sheep.nn.get_params().keys():
        if random() < MUTATION_RATE:
            sheep.nn.get_params()[param] += np.random.normal(0, MUTATION_SCALE)
    return sheep

def mutate_wolf(wolf):
    for param in wolf.nn.get_params().keys():
        if random() < MUTATION_RATE:
            wolf.nn.get_params()[param] += np.random.normal(0, MUTATION_SCALE)
    return wolf


def train_population():
    env = Environment()
    population = None

    best_sheep_fitness = -float("inf")
    best_sheep = None
    best_wolf_fitness = -float("inf")
    best_wolf = None
    
    sheep_fitness_history = []
    sheep_mean_fitness_history = []
    wolf_fitness_history = []
    wolf_mean_fitness_history = []
    
    for generation in range(NUM_GENERATIONS):
        env.spawn_entities(population=population)
        
        while not env.simulation_over:
            _, sheeps, wolfs = env.play_step()
            
        sheep_fitnesses = [fitness_function(s) for s in sheeps]
        best_current_sheep_fitness = max(sheep_fitnesses)
        sheep_fitness_history.append(max(sheep_fitnesses))
        sheep_mean_fitness_history.append(np.mean(sheep_fitness_history))
        
        wolf_fitnesses = [fitness_function(w) for w in wolfs]
        best_current_wolf_fitness = max(wolf_fitnesses)
        wolf_fitness_history.append(max(wolf_fitnesses))
        wolf_mean_fitness_history.append(np.mean(wolf_fitness_history))
        
        if best_current_sheep_fitness > best_sheep_fitness:
            best_sheep_fitness = best_current_sheep_fitness
            best_sheep = sheeps[sheep_fitnesses.index(best_sheep_fitness)]
            save_best_model(best_sheep, "sheep")
        if best_current_wolf_fitness > best_wolf_fitness:
            best_wolf_fitness = best_current_wolf_fitness
            best_wolf = wolfs[wolf_fitnesses.index(best_wolf_fitness)]
            save_best_model(best_wolf, "wolf")
        
        sheep_parents = select_parents(sheeps, SELECTED_ENTITY)
        wolf_parents = select_parents(wolfs, SELECTED_ENTITY)
        
        child_sheeps = [mutate_sheep(crossover_sheep(choice(sheep_parents), choice(sheep_parents))) for _ in range(SHEEP_POPULATION)]
        
        child_wolfs = [mutate_wolf(crossover_wolf(choice(wolf_parents), choice(wolf_parents))) for _ in range(WOLF_POPULATION)]
        
        # selected entties with highest fitness from both parents and children
        next_gen_sheeps = select_parents(sheeps + child_sheeps, SHEEP_POPULATION)
        next_gen_wolfs = select_parents(wolfs + child_wolfs, WOLF_POPULATION)
        
        population = next_gen_sheeps + next_gen_wolfs
        
        # Generate and save plots at the end of each generation
        plot_fitness(sheep_fitness_history, sheep_mean_fitness_history, wolf_fitness_history, wolf_mean_fitness_history)
        
        info_str = f"Generation {generation + 1} - Best sheep fitness: {best_current_sheep_fitness} - Best wolf fitness: {best_current_wolf_fitness}"
        log(info_str)
                
    pg.quit()
    sys.exit()
  