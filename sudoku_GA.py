
from SudokuProject.constants import GRID_SIZE
from objects.board import Board

def createPopulation(size: int):
    population = {Board().fillArea() for _ in range(size)}
    return population

def ranking(population):
    return sorted(population, key=lambda individual: individual.fitness())
gernation=createPopulation(5)
print(gernation)
for i in gernation:
    print(i.print())

print('-------------------------')
for i in ranking(gernation):
    print(i.print())

