import copy
from random import random

from SudokuProject.constants import GRID_SIZE
from objects.board import Board
import  numpy as np
def createPopulation(initBoard:Board,size: int)->list[Board]:
    population = {Board(initBoard.rows,initBoard.cols,initBoard.areas).fill_Board() for _ in range(size)}
    return population
def ranking_poppulation(population):
    return sorted(population, key=lambda individual: individual.fitness())
def selection(ranked_population,selection_rate:float,random_selection_rate:float)->list[Board]:
    ranked_population = ranking_poppulation(ranked_population)
    population_size = len(ranked_population)
    num_best_to_select = int(population_size * selection_rate)
    num_random_to_select = int(population_size * random_selection_rate)
    # Select the best elements
    selected_best = ranked_population[:num_best_to_select]
    # Select random elements
    selected_random = np.random.choice(ranked_population, num_random_to_select, replace=True)
    # Concatenate and shuffle the selected elements
    next_breeders = list(selected_best) + list(selected_random)
    np.random.shuffle(next_breeders)
    return next_breeders
def crossover(father:Board,mother:Board)->Board:
    elements_from_father = np.random.randint(0, GRID_SIZE, np.random.randint(1, GRID_SIZE - 1))
    child_areas = {}
    for i in range(GRID_SIZE):
        if i in elements_from_father:
            child_areas[i]=copy.deepcopy(father.areas[i])
        else:
            child_areas[i]=copy.deepcopy(mother.areas[i])
    child=Board(None,None,child_areas).update_Board_by_areas()
    return child
def breeds(population:list[Board],num_of_child)->Board:
    next_population = []
    population=ranking_poppulation(population)
    next_population.append(population[0])
    # Randomly pick 1 father and 1 mother until new population is filled
    range_val = int(len(population)/2) * num_of_child
    for _ in range(range_val):
        father = population[random.randint(2,range_val)]
        mother = population[random.randint(2,range_val)]
        while father==mother:
            father = population[random.randint(2, range_val)]
            mother = population[random.randint(2, range_val)]
        next_population.append(crossover(father, mother))
    return next_population
def mutation(population: list[Board], mutation_rate: float) -> list[Board]:
    # assert 0.0 <= mutation_rate <= 1.0, "mutation_rate should be in the range [0.0, 1.0]"
    population_with_mutation = []
    for individual in population:
        mutant_individual=copy.deepcopy(individual)
        if np.random.random() < mutation_rate: # random float number in the range [0.0, 1.0)
            mutant_individual.swap_update_2valid()
            #check whether a good mutant_individual or not if good add to population
        population_with_mutation.append(mutant_individual)
    return population_with_mutation


