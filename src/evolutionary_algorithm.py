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

def fitness_function(e: Entity, s: float, n: int):
    ENTITY_SURVIVAL_BONUS = 100
    SURVIVAL_BONUS = 1000

    entity_survival = (e.survival_time / GENERATION_DURATION) * ENTITY_SURVIVAL_BONUS
    generational_duration = (s / GENERATION_DURATION) * SURVIVAL_BONUS 
    
    return entity_survival + generational_duration


def select_parents(population, num_parents, sim_time, n_entities):
    population.sort(key=lambda x: fitness_function(x, sim_time, n_entities), reverse=True)
    return population[:num_parents]

def crossover_sheep(parent_1, parent_2):
    child_params = {}
    parent_1_params = list(parent_1.nn.get_params().items())
    parent_2_params = list(parent_2.nn.get_params().items())
    crossover_point = int(len(parent_1_params) / 2)
    
    for i in range(len(parent_1_params)):
        param_key = parent_1_params[i][0]
        if i <= crossover_point:
            child_params[param_key] = parent_1_params[i][1]
        else:
            child_params[param_key] = parent_2_params[i][1]
    
    return Sheep(parent_1.env, parent_1.env.sprite_manager, v2_0, NeuralNetwork(params=child_params))

def crossover_wolf(parent_1, parent_2):
    child_params = {}
    parent_1_params = list(parent_1.nn.get_params().items())
    parent_2_params = list(parent_2.nn.get_params().items())
    crossover_point = int(len(parent_1_params) / 2)
    
    for i in range(len(parent_1_params)):
        param_key = parent_1_params[i][0]
        if i <= crossover_point:
            child_params[param_key] = parent_1_params[i][1]
        else:
            child_params[param_key] = parent_2_params[i][1]
    
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
            sim_time, sheeps, wolfs, n_wolfs, n_sheeps = env.play_step()
            
        sheep_fitnesses = [fitness_function(s, sim_time, n_sheeps) for s in sheeps]
        best_current_sheep_fitness = max(sheep_fitnesses)
        sheep_fitness_history.append(best_current_sheep_fitness)
        sheep_mean_fitness_history.append(np.mean(sheep_fitness_history))
        
        wolf_fitnesses = [fitness_function(w, sim_time, n_wolfs) for w in wolfs]
        best_current_wolf_fitness = max(wolf_fitnesses)
        wolf_fitness_history.append(best_current_wolf_fitness)
        wolf_mean_fitness_history.append(np.mean(wolf_fitness_history))
        
        if best_current_sheep_fitness > best_sheep_fitness:
            best_sheep_fitness = best_current_sheep_fitness
            best_sheep = sheeps[sheep_fitnesses.index(best_sheep_fitness)]
            save_best_model(best_sheep, "sheep")
        if best_current_wolf_fitness > best_wolf_fitness:
            best_wolf_fitness = best_current_wolf_fitness
            best_wolf = wolfs[wolf_fitnesses.index(best_wolf_fitness)]
            save_best_model(best_wolf, "wolf")
        
        sheep_parents = select_parents(sheeps, SELECTED_ENTITY, sim_time, n_sheeps)
        wolf_parents = select_parents(wolfs, SELECTED_ENTITY, sim_time, n_wolfs)
        
        child_sheeps = [mutate_sheep(crossover_sheep(choice(sheep_parents), choice(sheep_parents))) for _ in range(SHEEP_POPULATION - SELECTED_ENTITY)]
        child_wolfs = [mutate_wolf(crossover_wolf(choice(wolf_parents), choice(wolf_parents))) for _ in range(WOLF_POPULATION - SELECTED_ENTITY)]
        
        next_gen_sheeps = sheep_parents + child_sheeps
        next_gen_wolfs = wolf_parents + child_wolfs
        
        population = next_gen_sheeps + next_gen_wolfs
        
        # Generate and save plots at the end of each generation
        plot_fitness(sheep_fitness_history, sheep_mean_fitness_history, wolf_fitness_history, wolf_mean_fitness_history)
        
        info_str = f"Generation {generation + 1} - Best sheep fitness: {best_current_sheep_fitness} - Best wolf fitness: {best_current_wolf_fitness}"
        log(info_str)
                
    pg.quit()
    sys.exit()
