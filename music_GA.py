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

verhouding_stabiel_instabiel = 1  # a
straf_te_willekeurig = 2  # S
straf_te_saai = -2  # p

bonus_correcte_opvolging = 2  # R
straf_incorrecte_opvolging = 2  # q

b = 2
Q = 2
V = -2

straf_tritonus = 2  # V
straf_sext = 3  # W
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


def nr_instable_notes(chromosome, chord):
    pass


def fitness_stable_instable_notes():
    pass


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
        if i % length_chromosome:
            new_genotype.append(new_chromosome)
            new_chromosome = ""
        
        new_chromosome += str("".join(parents[current_gene_donor].genotype)[i])
    
    print(new_genotype)

crossover([Melody(create_random_genotype(), 0), Melody(create_random_genotype(), 0)], 0)
