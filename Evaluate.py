import time
import os
import sys
import traceback
import pathlib
import psutil
import matplotlib.pyplot as plt

from model.Configuration import Configuration
from algorithm.Amga2 import Amga2 
from algorithm.Emosoa import Emosoa
from algorithm.GeneticAlgorithm import GeneticAlgorithm
from algorithm.Hgasso import Hgasso
from algorithm.Ngra import Ngra
from algorithm.NsgaII import NsgaII

def evaluate_algorithm(algorithm, configuration):
    start_time = time.time()
    start_mem = psutil.Process(os.getpid()).memory_info().rss / 1024.0 / 1024.0

    alg_instance = algorithm(configuration)
    numGeneration = alg_instance.run()

    end_time = time.time()
    end_mem = psutil.Process(os.getpid()).memory_info().rss / 1024.0 / 1024.0

    exec_time = end_time - start_time
    mem_usage = end_mem - start_mem
    num_generations = numGeneration  

    return exec_time, mem_usage, num_generations

def main():
    algorithms = {
        'Amga2': Amga2,
        'Emosoa': Emosoa,
        'GeneticAlgorithm': GeneticAlgorithm,
        'Hgasso': Hgasso,
        'Ngra': Ngra,
        'NsgaII': NsgaII
    }

    results = {alg_name: {'exec_time': [], 'mem_usage': [], 'num_generations': []} for alg_name in algorithms}

    for i in range(25):  # 25 datasets
        file_name = f"/GaSchedule_subset_{i+1}.json"
        target_file = str(pathlib.Path().absolute()) + file_name
        configuration = Configuration()
        configuration.parseFile(target_file)

        for alg_name, alg_class in algorithms.items():
            try:
                exec_time, mem_usage, generations = evaluate_algorithm(alg_class, configuration)
                results[alg_name]['exec_time'].append(exec_time)
                results[alg_name]['mem_usage'].append(mem_usage)
                results[alg_name]['num_generations'].append(generations)
                print(f"{alg_name} on dataset {i+1}")
            except Exception as e:
                traceback.print_exc()
                print(f"Error occurred while evaluating {alg_name} on dataset {i+1}: {e}")

    # Plotting Execution Time
    plt.figure(figsize=(15, 5))
    for alg_name, data in results.items():
        plt.plot(range(1, 21), data['exec_time'], marker='o', label=alg_name)
    plt.xlabel('Dataset')
    plt.ylabel('Execution Time (s)')
    plt.title('Execution Time for Each Algorithm')
    plt.legend()
    plt.show()

    # Plotting Memory Usage
    plt.figure(figsize=(15, 5))
    for alg_name, data in results.items():
        plt.plot(range(1, 21), data['mem_usage'], marker='o', label=alg_name)
    plt.xlabel('Dataset')
    plt.ylabel('Memory Usage (MB)')
    plt.title('Memory Usage for Each Algorithm')
    plt.legend()
    plt.show()

    # Plotting Number of Generations
    plt.figure(figsize=(15, 5))
    for alg_name, data in results.items():
        plt.plot(range(1, 21), data['num_generations'], marker='o', label=alg_name)
    plt.xlabel('Dataset')
    plt.ylabel('Number of Generations')
    plt.title('Number of Generations for Each Algorithm')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
