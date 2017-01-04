import re
from random import randint

""" -------------------------- Parameters ----------------------------------"""

population_size = 100
mutation_rate = 0.02
number_of_candidate_solutions = 4
elite_selection = 5
crossover_type = "n_points_crossover"
crossover_points = 2

nr_chromosomes = 8
length_chromosome = 8

proportion_stable_unstable = 10 # T, ideal amount of unstable notes is proportion_stable_unstable times as much as amount of stable notes
a = 1  # a
punish_unstable = 2  # S, the punishment for the excess of instable notes
punish_stable = -2  # p, the punishment for the excess of stable notes
bonus_T_zero = 15 # the bonus when the proportion between stable and unstables notes is ideal

R = 2  # R
q = 2  # q

b = 2
Q = 2
V = -2

V = 3  # V
W = 2  # W
straf_septime = 5 # X


"""---------------------- defining representation --------------------------"""


class Melody(object):
    def __init__(self, genotype, generation):
        #Initiates the Melody, takes a.o. a list of chromosomes as input. 

        assert type(generation) is int \
                and type(genotype) is list \
                and all([type(chromosome) is str
                         and len(chromosome) is length_chromosome
                         and len(genotype) is nr_chromosomes
                         and re.search(r'[^0-9A-F]', chromosome) is None
                         for chromosome in genotype])\
                and len(genotype) is nr_chromosomes,\
                "Invalid Melody input"

        self.genotype = genotype
        self.generation = generation
        self.fitness = 0

def create_random_genotype():
    #creates a random genotype, consisting of chromosomes of type string
    genotype = []
    for chromosome_nr in range(nr_chromosomes):
        chromosome = ""
        for gene_nr in range(length_chromosome):
            chromosome += str(hex(randint(0, 15)))[2::].upper()
        genotype.append(chromosome)
    return genotype

"""------------------------- Fitness ---------------------------------------"""

notes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", 'D', 'E', 'F']
stable_notes = {"Am": ["1", "3", "6", "8", "A", "D"],
                "C": ["1", "3", "5", "8", "A", "C"],
                "F": ["1", "4", "6", "8", "B", "D"],
                "G": ["2", "5", "7", "9", "C", "E"],
                "Em": ["3", "5", "7", "A", "C", "E"],
                "Dm": ["2", "4", "6", "9", "B", "D"]}
                
instable_notes = {"Am": ["7", "9", "B", "C", "E", "2", "4", "5"],
                  "C": ["2", "4", "6", "7", "9", "B", "D", "E"],
                  "F": ["5", "7", "9", "A", "C", "E", "2", "3"],
                  "G": ["6", "8", "A", "B", "D", "1", "3", "4"],
                  "Em": ["4", "6", "8", "9", "B", "D", "1", "2"],
                  "Dm": ["3", "5", "7", "8", "A", "C", "E", "1"]}

def fitness_stable_unstable_notes(chromosome, chord):
    assert type(chord) is str and type(chromosome) is str, "invalid input"
    
    stable, unstable, fitness = 0, 0, 0
    
    for i in chromosome:
        if i in stable_notes[chord]:
            stable += 1
        elif i in instable_notes[chord]:
            unstable += 1
    
    T = stable - proportion_stable_unstable * unstable
    
    if T > 0:
        fitness -= punish_stable * T
    elif T < 0:
        fitness -= punish_unstable * T
    else:
        fitness += bonus_T_zero
    return fitness

print(fitness_stable_unstable_notes("357A1246", "Dm"))
    
def fitness_steps():
    pass


def fitness_note_length():
    pass


def fitness(individual):
    """
        Returns the fitness of the given individual.
    """
    assert type(individual) is Melody, "invalid input"

    individual.fitness = 1000
    return individual.fitness

"""------------------------ Reproduction -----------------------------------"""

def select_parents(population):
    """
     The parameter population is a list of instances of the class Melody.
     This function should return a list of two Melody objects that
     have been selected to be a parent.

     This function takes a group of number_of_candidate_solutions
     random individuals and selects the two best candidates.
    """
    assert type(population) is list and len(population) is population_size \
        and all([type(n) is Melody for n in population]), \
        "Invalid population"

    candidate_parents = [population[randint(0, len(population) - 1)] for x in range(number_candidate_parents)]
    sorted(candidate_parents, key=lambda solution: solution.fitness)[::-1]
    return [candidate_parents[0], candidate_parents[1]]


def crossover(parents, generation):
    """
        Creates a new genotype from the DNA of the parents.
        It takes crossover_points points in the genotypes of the parents,
        and constructs a new genotype.
    """

    assert len(parents) is 2 and all([type(n) is Melody for n in parents]),\
        "invalid parents"

    index_crossover_points = [randint(1, length_chromosome*nr_chromosomes)
                              for i in range(crossover_points)]
    while len(set(index_crossover_points)) != len(index_crossover_points):
        index_crossover_points = [randint(1, length_chromosome*nr_chromosomes)
                                  for i in range(crossover_points)]
    index_crossover_points.sort()
    
    current_gene_donor = randint(0, 1)
    new_genotype = []
    new_chromosome = ""
    for i in range(length_chromosome*nr_chromosomes):
        if i in index_crossover_points:
            current_gene_donor = not current_gene_donor
        if i % length_chromosome is 0 and i is not 0:
            new_genotype.append(new_chromosome)
            new_chromosome = ""
        
        new_chromosome += "".join(parents[current_gene_donor].genotype)[i]
    new_genotype.append(new_chromosome)
    
    return Melody(new_genotype, generation)

def mutation(individual):
    """
        Changes a note to a random note with a chance of mutation_rate
    """
    assert type(individual) is Melody, "invalid individual"

    genotype = individual.genotype
    chromosome_nr = 0
    for chromosome in genotype:
        chromosome = list(chromosome)
        
        for i in range(length_chromosome):
            if randint(0, 100)/100 < mutation_rate:
                chromosome[i] = str(hex(randint(0, 15)))[2::].upper()

        chromosome = "".join(chromosome)
        genotype[chromosome_nr] = chromosome
        chromosome_nr += 1
    individual.genotype = genotype
    return individual


def elite(population):
    """
     Returns the elite of the population.
    """
    assert all([type(x) is Melody for x in population])
    if elite_selection is 0:
        return []
    
    sorted_population = sorted(population, key=lambda solution: solution.fitness)
    return sorted_population[-elite_selection:]

