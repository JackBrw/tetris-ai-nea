#The code will be a genetic algorithm that will solve or attempt to solve a very complex equation
import math
import random as rnd
import decimal as dec
import time

population = []

def equation(w, x, y, z):
    return 12*w**5 + 15*x**-2 + 4*y - z**3 - 350 #EQUATION => 12w^5 + 9x^-2 + 23y - z^3 = 350

def fitness(values): #Sees how close the answer is to 0 i.e the correct answer
    w, x, y, z = values
    ans = equation(w, x, y, z)
    return abs(1/ans)

class Genome(): #pretty much just a class that hold 4 values
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def getValues(self):
        return self.w, self.x, self.y, self.z

    def setValues(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

def generate_population(no_of_genomes): #edits the population list to add a specified number of genomes
    for x in range(no_of_genomes):      #and gives each genome 4 random values for the equation
        population.append(Genome(rnd.random(), rnd.random(), rnd.random(), rnd.random()))

def order():
    popFitness = [] #array of all fitness values of the genomes (the values they will be ordered by)
    for obj in population:
        popFitness.append(fitness(obj.getValues()))
    loop = True
    while loop:
        loop = False
        for i in range(0, len(popFitness) - 1): #bubble sort algorithm, for larger population sizes it is not good
            temp = popFitness[i]
            temp1 = population[i]
            if popFitness[i + 1] > popFitness[i]:
                popFitness[i] = popFitness[i + 1]
                popFitness[i + 1] = temp
                population[i] = population[i + 1]
                population[i + 1] = temp1 
                loop = True

def evolve(): #fairly inefficient evolving method
    w1, x1, y1, z1 = population[0].getValues()
    w2, x2, y2, z2 = population[1].getValues()
    newGenome = []
    for i in range(2, len(population)):
        oneCount = 0  #one count and zero count make sure that each child genome inherits two values from each parent
        zeroCount = 0
        newGenome = [2, 2, 2, 2]
        for j in range(0, 3):
            if oneCount >= 2:
                newGenome[j] = 0
                zeroCount += 1
            elif zeroCount >= 2:
                newGenome[j] = 1
                oneCount += 1
            else:
                newGenome[j] = rnd.randint(0, 1)
                if newGenome[j] == 1:
                    oneCount += 1
                else:
                    zeroCount += 1
        
        if newGenome[0] == 0: #assigning each genome its new values
            newGenome[0] = w1
        else:
            newGenome[0] = w2
        if newGenome[1] == 0:
            newGenome[1] = x1
        else:
            newGenome[1] = x2
        if newGenome[2] == 0:
            newGenome[2] = y1
        else:
            newGenome[2] = y2
        if newGenome[3] == 0:
            newGenome[3] = z1
        else:
            newGenome[3] = z2
        
        for x in range(0,4 ): #mutating the values 10% chance
            chance = 10
            value = rnd.randint(1, 100)
            if value <= chance:
                newGenome[x] += float(dec.Decimal(rnd.randrange(-10000, 10000))/100000)
        population[i].setValues(newGenome[0],newGenome[1],newGenome[2],newGenome[3])

def showPopulation(x):
        for i in range(0, x):
            w, x, y, z = population[i].getValues()
            print(f"{population[i].getValues()} ||| {fitness(population[i].getValues())} ||| {equation(w, x, y, z)}")

generate_population(int(input("Population size: ")))
while __name__ == "__main__":
    x = int(input("Number of generations: "))
    start = time.time()
    for i in range(1, x):
        order()
        evolve()
    end = time.time()
    order()
    num = int(input("How many genomes: "))
    showPopulation(num)
    print(f"{end - start}s")