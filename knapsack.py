"""

Knapsack problem by Joos and Tim

ITEM	        survivalpoints 	  weight (kg)

beans 	      20.00 	        05.00
coffee            5.00               04.00 
compass 	      30.00 	        01.00
pocketknife 	10.00 	        01.00
potatoes 	      15.00 	        10.00
rope        	10.00 	        05.00
sleeping bag 	30.00 	        07.00
unions 	      2.00 	              01.00



"""
from random import randint
from inspect import isfunction
import GraphImport
""" 
----------------------------- defining the items ------------------------------ 
"""

class Item(object):
    def __init__(self, value, weight):
        self.weight = weight
        self.value = value

beans = Item(20.0, 5.0)
book = Item(4.0, 6.0)
coffee = Item(5.0, 4.0)
compass = Item(30.0, 1.0)
dictionary = Item(1.0, 8.0)
pocketknife = Item(10.0, 1.0)
potatoes = Item(15.0, 10.0)
rope = Item(10.0, 5.0)
sleeping_bag = Item(30.0, 7.0)
unions = Item(2.0, 1.0)
items = [beans, book, coffee, compass, dictionary, pocketknife, potatoes, rope, sleeping_bag, unions]
nr_of_items = len(items)


""" 
-------------------------- defining the parameters ---------------------------- 
"""


population_size = 100
number_of_generations = 100
number_candidate_parents = 5 #See explanation of the select_parent_solutions function
mutation_rate = 0.02 #Chance of a bit in the genotype getting flipped 
elite_selection = 5 # Size of the elitist selection


"""
---------------------------- initiating population ----------------------------
"""


class PossibleSolution(object):
    def __init__(self, genotype):
        assert len(genotype) is len(items) and type(genotype) is str, "Invalid genotype"
        self.genotype = genotype
        
    def fitness_function(self):
        """    
         Calculates the fitness of the solution.
         This is equal to the combined value of the content of the 
         knapsack if the weight is under 20. If it is higher, 
         the fitness will decrease with (20 - weight) * 10 points.
         e.g. a weight of 22 would result in a penalty of 20 points 
        """
        index = 0
        total_weight = 0
        total_value = 0
        for i in self.genotype:
            if i == "1":
                total_value += items[index].value
                total_weight += items[index].weight
            index += 1
            
        if(total_weight > 20):
            self.fitness = total_value + (20 - total_weight) * 10
        else:
            self.fitness = total_value
        return (self.fitness)

def create_random_genotype():
    # Create a string of random binary digits of length nr_of_items
    random_genotype = "".join([str(randint(0,1)) for x in range(nr_of_items)])
    return random_genotype



"""
--------------------- defining the procedure for reproduction -----------------
"""


def select_parent_solutions(population):
    """
     The parameter population is a list of instances of the class PossibleSolution.
     This function should return a list of two PossibleSolution objects which 
     have been selected to be a parent.
     
     This function takes a group of n random individuals and selects the two
     best candidates.
    """
    assert type(population) is list and len(population) is population_size \
            and all([type(n) is PossibleSolution for n in population]), \
            "Invalid population"
            
    candidate_parents = [population[randint(0, number_candidate_parents)] for x in range(5)]
    sorted(candidate_parents, key=lambda solution: solution.fitness)[::-1]
    return [candidate_parents[0], candidate_parents[1]]

def n_points_crossover(parents, n):
    """
     This function should only be called by the crossover function. 
     It returns a PossibleSolution with a combination of the parental genotypes.
    """
    assert n < len(items) and n >= 0 and len(parents) is 2, "invalid amount of crossover points"
    
    crossover_points = [randint(1, len(items) - 1) for x in range(n)]
    while len(set(crossover_points)) != len(crossover_points):
        # To make sure that there are n crossoverpoints
        crossover_points = [randint(1, len(items) - 1) for x in range(n)]
    crossover_points.sort()
    
    current_gene_donor = randint(0, 1)
    new_genotype = ""
    for i in range(len(items)):
        new_genotype += parents[current_gene_donor].genotype[i]
        if i + 1 in crossover_points:
            current_gene_donor = not current_gene_donor
    
    return PossibleSolution(new_genotype)
    
def universal_crossover(parents, n):
    """
     This function should only be called by the crossover function.
     It returns a PossibleSolution with a random combination of the parental genotypes.
    """    
    assert len(parents) is 2, "Invalid amount of parents"
    new_genotype = ""
    for i in range(len(items)):
        current_gene_donor = randint(0, 1)
        new_genotype += parents[current_gene_donor].genotype[i]
        
    return PossibleSolution(new_genotype)
    
def crossover(parent_0, parent_1, crossover_type, nr_crossover_points=0):
    """
     Parent_0 and parent_1 are the instances of PossibleSolution which have been
     selected for reproduction.
     There are two functions with two seperate ways of performing crossover
     (universal_crossover and n_points_crossover).
     
    """
    assert type(parent_0) is PossibleSolution and type(parent_1) is PossibleSolution \
          and isfunction(crossover_type), "invalid type of the two parents"

    return crossover_type([parent_0, parent_1], nr_crossover_points)
    
def mutation(individual):
    """
     Flips a bit in the genotype with a chance of mutation_rate
    """    
    assert type(individual) is PossibleSolution, "individual must be PossibleSolution"
    genotype = list(individual.genotype)
    
    for i in range(nr_of_items):
        if randint(0,100)/100 < mutation_rate:
            genotype[i] = str(int(not bool(genotype[i])))
    individual.genotype = "".join(genotype)
    return individual

def elite(population):
    """
     Returns the elite of the population.
    """
    if elite_selection is 0:
        return []
    
    sorted_population = sorted(population, key=lambda solution: solution.fitness)
    return sorted_population[-elite_selection:]


"""
--------------------------------- The real magic ------------------------------
"""

graph_data = []
population = [PossibleSolution(create_random_genotype()) for i in range(population_size)]
fitnesses = [member.fitness_function() for member in population]



for generation in range(number_of_generations):
    
    graph_data.append([generation, sum(fitnesses)/float(len(fitnesses))])    
    
    new_population = []
    new_population.extend(elite(population)) #Adds the elite of the previous generation to the current
    
    for i in range(population_size - elite_selection):
        parents = select_parent_solutions(population) #Select parents
        new_individual = crossover(parents[0], parents[1], n_points_crossover, 1) #Combine their genes
        new_individual = mutation(new_individual) # Mutate (small chance, though)
        new_population.append(new_individual) 
   
    population = new_population
    fitnesses = [member.fitness_function() for member in population]
    
   


argv = ['', '-i', graph_data, '-o', "average.jpg", '-x', [0, population_size], '-y', [0,105], '--xti', 5, '--yti', 5] 
GraphImport.main(argv)

















