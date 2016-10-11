"""

Knapsack problem

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

####################### PARAMETERS #######################

population_size = 100

##########################################################

""" 
    <defining the items> 
"""

class Item(object):
    def __init__(self, value, weight):
        self.weight = weight
        self.value = value

beans = Item(20.0, 5.0)
coffee = Item(5.0, 4.0)
compass = Item(30.0, 1.0)
pocketknife = Item(10.0, 1.0)
potatoes = Item(15.0, 10.0)
rope = Item(10.0, 5.0)
sleeping_bag = Item(30.0, 7.0)
unions = Item(2.0, 1.0)
items = [beans, coffee, compass, pocketknife, potatoes, rope, sleeping_bag, unions]


"""
    <initiating population>
"""

class PossibleSolution(object):
    def __init__(self, genotype):
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
    # Create a string of random binary digits of length 8
    random_genotype = "".join([str(randint(0,1)) for x in range(8)])
    return random_genotype

population = [PossibleSolution(create_random_genotype()) for i in range(population_size)]
fitnesses = [member.fitness_function() for member in population]































