from .NsgaII import NsgaII
from time import time
import numpy as np
from random import random

# https://www.researchgate.net/publication/241105578_Non-dominated_ranked_genetic_algorithm_for_solving_multi-objective_optimization_problems_NRGA

# Non-dominated Ranking Genetic Algorithm (NRGA) 
class Ngra(NsgaII):
    def __init__(self, configuration, numberOfCrossoverPoints=2, mutationSize=2, crossoverProbability=80,
                 mutationProbability=3):
        NsgaII.__init__(self, configuration, numberOfCrossoverPoints, mutationSize, crossoverProbability, mutationProbability)
        
    @staticmethod    
    def __cumulative(lists): 
        cu_list = [] 
        length = len(lists) 
        cu_list = [sum(lists[0:x:1]) for x in range(0, length+1)] 
        return cu_list[1:]
        
    def replacement(self, population):
        populationSize = self._populationSize
        numberOfCrossoverPoints = self._numberOfCrossoverPoints
        crossoverProbability = self._crossoverProbability
        
        obj = {m: population[m].fitness for m in range(populationSize)}
        sortedIndices = list(reversed(sorted(obj, key=obj.get)))
        totalFitness = (populationSize + 1) * populationSize / 2
        probSelection = [i / totalFitness for i in range(populationSize)]
        cumProb = self.__cumulative(probSelection)
        selectIndices = [random() for i in range(populationSize)]
        parent = 2 * [None]
        parentIndex = 0        
        offspring = []
        for i in range(populationSize):
            selected = False
            for j in range(populationSize - 1):
                if cumProb[j] < selectIndices[i] and cumProb[j + 1] >= selectIndices[i]:
                    parent[parentIndex % 2] = population[sortedIndices[j + 1]]
                    parentIndex += 1
                    selected = True
                    break
                    
            if not selected:
                parent[parentIndex % 2] = population[sortedIndices[i]]
                parentIndex += 1
                
            if parentIndex % 2 == 0:
                child0 = parent[0].crossover(parent[1], numberOfCrossoverPoints, crossoverProbability)
                child1 = parent[1].crossover(parent[0], numberOfCrossoverPoints, crossoverProbability)
                offspring.extend((child0, child1))
            
        return offspring
        
    def initialize(self, population):
        super().initialize(population)
        offspring = self.replacement(population)
        population.clear()
        population.extend(offspring)
        
    def run(self, maxRepeat=9999, minFitness=0.999):
        mutationSize = self._mutationSize
        mutationProbability = self._mutationProbability
        nonDominatedSorting = self.nonDominatedSorting
        selection = self.selection
        populationSize = self._populationSize
        population = populationSize * [None]

        self.initialize(population)
        random.seed(round(time() * 1000))
        np.random.seed(int(time()))

        currentGeneration = 0

        repeat = 0
        lastBestFit = 0.0

        while 1:
            if currentGeneration > 0:
                best = self.result
                print("Fitness:", "{:f}\t".format(best.fitness), "Generation:", currentGeneration, end="\r")

                if best.fitness > minFitness:
                    break

                difference = abs(best.fitness - lastBestFit)
                if difference <= 0.0000001:
                    repeat += 1
                else:
                    repeat = 0

                self._repeatRatio = repeat * 100 / maxRepeat
                if repeat > (maxRepeat / 100):
                    self.reform()

            # crossover
            offspring = self.replacement(population)

            # mutation
            for child in offspring:
                child.mutation(mutationSize, mutationProbability)

            totalChromosome = population + offspring

            # non-dominated sorting
            front = nonDominatedSorting(totalChromosome)
            if len(front) == 0:
                break

            # selection
            population = selection(front, totalChromosome)
            self._populationSize = populationSize = len(population)

            # comparison
            if currentGeneration == 0:
                self._chromosomes = population
            else:
                totalChromosome = population + self._chromosomes
                newBestFront = nonDominatedSorting(totalChromosome)
                if len(newBestFront) == 0:
                    break
                self._chromosomes = selection(newBestFront, totalChromosome)
                lastBestFit = best.fitness

            currentGeneration += 1
        
    def __str__(self):
        return "Non-dominated Ranking Genetic Algorithm (NRGA)"
             