import matplotlib.pyplot as plt
import os

os.makedirs("models", exist_ok=True)

def save_best_model(model, name):
    count = len(os.listdir("models"))
    filename = f"models/{name}_{count + 1}.model"
    model.save(filename)

os.makedirs("logs", exist_ok=True)
count = len(os.listdir("logs"))
log_file_path = f"logs/generation_log_{count + 1}.txt"

def log(message):
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")
    

def plot_fitness(sheep_fitness_history, sheep_mean_fitness_history, wolf_fitness_history, wolf_mean_fitness_history):
    plt.figure()
    plt.plot(sheep_fitness_history, label="Best Sheep Fitness")
    plt.plot(sheep_mean_fitness_history, label="Mean Sheep Fitness")
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig('src/static/sheep_plot.png')
    plt.close()

    plt.figure()
    plt.plot(wolf_fitness_history, label="Best Wolf Fitness")
    plt.plot(wolf_mean_fitness_history, label="Mean Wolf Fitness")
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig('src/static/wolf_plot.png')
    plt.close()