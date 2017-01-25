# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 19:50:35 2017
"""

from random import random, randint
import re
from random import randint

""" -------------------------- Parameters ----------------------------------"""

population_size = 100
mutation_rate = 0.02
number_of_candidate_solutions = 4
elite_selection = 5
crossover_type = "n_points_crossover"
crossover_points = 2

crossover_chance = 0.3
number_of_generations = 100

nr_chromosomes = 8
length_chromosome = 8

chords = ["C", "Am", "F", "G", "Em", "Am", "Dm", "G"]

proportion_stable_unstable = 1 # T, ideal amount of unstable notes is proportion_stable_unstable times as much as amount of stable notes
a = 1  # a
punishment_unstable = -2  # S, the punishment for the excess of instable notes
punishment_stable = 2  # p, the punishment for the excess of stable notes
bonus_T_zero = 15 # the bonus when the proportion between stable and unstables notes is ideal

punishment_rest = 15
punishment_invalid_succession = 10

punishment_steps_leaps = 10
punishment_big_leaps = 10
bonus_steps_leaps = 20
proportion_steps_leaps = 1
punishment_sext = 20
punishment_septime = 15

"""---------------------- defining representation --------------------------"""
note_representation = {
                       "0": "-",  # rust
                       "1": "C5",
                       "2": "D5",
                       "3": "E5",
                       "4": "F5",
                       "5": "G5",
                       "6": "A5",
                       "7": "B5",
                       "8": "C6",
                       "9": "D6",
                       "A": "E6",
                       "B": "F6",
                       "C": "G6",
                       "D": "A6",
                       "E": "B6",
                       "F": "."  # aanhouden van de noot
                       }

def genotype_to_fenotype(genotype):
    """
        Returns the names of the note the gene represents
        e.g. a 1 in our representation is the note C
    """
    fenotype = []
    for chromosome in genotype:
        fenotype_of_chromosome = ""
        for note in chromosome:
            fenotype_of_chromosome += note_representation[note]
        fenotype.append(fenotype_of_chromosome)
    return fenotype


class Melody(object):
    def __init__(self, genotype, generation):
        """
            Initiates the Melody
            Takes a list of chromosomes and the current generation as input. 
        """

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
        self.chromosome_fitnesses = [0]*nr_chromosomes

def create_random_genotype():
    """
        creates a random genotype, consisting of chromosomes of type string
    """
    genotype = []
    for chromosome_nr in range(nr_chromosomes):
        chromosome = ""
        for gene_nr in range(length_chromosome):
            chromosome += str(hex(randint(0, 15)))[2::].upper()
        genotype.append(chromosome)

    return genotype

"""------------------------- Fitness ---------------------------------------"""

notes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", 'D', 'E', 'F']
stable_notes = {"Am": ["6", "8", "A", "D","1", "3"],
                "C": ["1", "3", "5", "8", "A", "C"],
                "F": [ "4", "6", "8", "B", "D", "1"],
                "G": ["5", "7", "9", "C", "E", "2"],
                "Em": ["3", "5", "7", "A", "C", "E"],
                "Dm": ["2", "4", "6", "9", "B", "D"]}
                
instable_notes = {"Am": ["7", "9", "B", "C", "E", "2", "4", "5"],
                  "C": ["2", "4", "6", "7", "9", "B", "D", "E"],
                  "F": ["5", "7", "9", "A", "C", "E", "2", "3"],
                  "G": ["6", "8", "A", "B", "D", "1", "3", "4"],
                  "Em": ["4", "6", "8", "9", "B", "D", "1", "2"],
                  "Dm": ["3", "5", "7", "8", "A", "C", "E", "1"]}

def fitness_stable_unstable_notes(chromosome, chord):
    """
        Input: the current chromosome, the current chord
        This function returns the decrease in fitness of a piece of music
        due to an imbalance in stable and unstable notes.
    """
    assert type(chord) is str and type(chromosome) is str, "invalid input"
    
    stable, unstable, fitness = 0, 0, 0
    
    for i in chromosome:
        if i in stable_notes[chord]:
            stable += 1
        elif i in instable_notes[chord]:
            unstable += 1
    
    T = stable - proportion_stable_unstable * unstable
    
    if T > 0:
        fitness -= punishment_stable * T
    elif T < 0:
        fitness -= punishment_unstable * T
    else:
        fitness += bonus_T_zero
    return fitness


def next_tone(chromosome, current_index, return_new_index=False):
    """
        Returns the next gene in the chromosome, or "error" if there is none.
        (because there are characters (0 and F) that need to be ignored)
    """
    assert type(chromosome) is str and len(chromosome) is length_chromosome\
        and current_index < length_chromosome,\
        "invalid chromosome"

    i = current_index + 1
    while re.search(r"[F0]", chromosome[i:i+1:]) is not None and i < length_chromosome:
        i += 1
    if i is 8:
        return "error"
    elif not return_new_index:
        return chromosome[i]
    else:
        return (chromosome[i], i)


def fitness_note_length(chromosome):
    """
    """
    rest = chromosome.count("F") + chromosome.count("0")
    if rest < 3:
        rest = 7 - rest
    if rest >= 3 and rest < 5:
        rest = 0
    return - (rest * punishment_rest)


def fitness_note_after_instable_tone(chord, chromosome):
    
    fitness = 0
    for i in range(len(chromosome)):
        if chromosome[i] in instable_notes[chord]:
            interval = instable_notes[chord].index(chromosome[i])
            if interval in [0, 4]: #secunde
                if next_tone(chromosome, i) not in [stable_notes[chord][0],
                                                    stable_notes[chord][1],
                                                    stable_notes[chord][3],
                                                    stable_notes[chord][4]]:
                    fitness -= punishment_invalid_succession
            elif interval in [1, 5]:  # kwart
                if next_tone(chromosome, i) not in [stable_notes[chord][1],
                                                    stable_notes[chord][4]]:
                     fitness -= punishment_invalid_succession
            elif interval in [2, 6]:  # sext
                if next_tone(chromosome, i) not in [stable_notes[chord][2],
                                                    stable_notes[chord][5]]:
                    fitness -= punishment_invalid_succession
            elif interval in [3, 7]:  # septiem
                if next_tone(chromosome, i) not in [stable_notes[chord][0],
                                                    stable_notes[chord][3]]:
                    fitness -= punishment_invalid_succession
    return fitness


def fitness_note_leaps(chromosome):

    current_note = next_tone(chromosome, -1)
    note_index = next_tone(chromosome, -1, True)[1]
    leaps, steps, fitness = 0, 0, 0

    while current_note != "error" and next_tone(chromosome, note_index) != "error":
        next_note = next_tone(chromosome, note_index)
        interval = abs(notes.index(current_note) - notes.index(next_note)) + 1
        if interval <= 2:
            #print("step")
            steps += 1
        else:
            leaps += 1
            #print("leap")

        if interval is 6:
            fitness -= punishment_sext
            #print("sext")
        elif interval is 7:
            fitness -= punishment_septime
            #print("septime")
        elif interval > 8:
            fitness -= punishment_big_leaps
            #print("big leap")
        current_note = next_tone(chromosome, note_index)
        note_index = next_tone(chromosome, note_index, True)[1]
    
    T = steps - proportion_steps_leaps * leaps
    if T is 0:
        fitness += bonus_steps_leaps
    else:
        fitness -= abs(T)*punishment_steps_leaps
    return fitness

def fitness(individual):
    """
        Returns the fitness of the given individual.
    """
    assert type(individual) is Melody, "invalid input"

    individual.fitness = 1000
    for chromosome_index in range(len(individual.genotype)):
        chromosome_fitness = 0
        chromosome_fitness += fitness_note_after_instable_tone\
                                    (chords[chromosome_index],
                                     individual.genotype[chromosome_index])
        chromosome_fitness += fitness_stable_unstable_notes\
                                    (individual.genotype[chromosome_index],
                                     chords[chromosome_index])
        chromosome_fitness += fitness_note_length(individual.genotype[chromosome_index])
        chromosome_fitness += fitness_note_leaps(individual.genotype[chromosome_index])
        individual.fitness += chromosome_fitness
        individual.chromosome_fitnesses[chromosome_index] = chromosome_fitness
        
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
    
    assert type(population) is list and len(population) == population_size\
        and all([type(n) is Melody for n in population]), \
        "Invalid population"

    candidate_parents = [population[randint(0, len(population) - 1)] for x in range(number_of_candidate_solutions)]
    sorted(candidate_parents, key=lambda solution: solution.fitness)[::-1]
    return [candidate_parents[0], candidate_parents[1]]


def crossover(parents, generation):
    """
        Combines the DNA of both parents to create a new Melody.
        Input: a list of two parent Melodies, the generation (int)
        In every chromosome, there is a crossover_chance chance of occurence
        of crossover. Otherwise, it will take the best chromosome of both 
        parents.
    """
    new_genotype = [""]*nr_chromosomes

    for chromosome_index in range(length_chromosome):

        if(random() < crossover_chance):
            crossover_point = randint(0, (length_chromosome))
            current_gene_donor = randint(0, 1)

            for allel_index in range(length_chromosome):
                if allel_index == crossover_point:
                    current_gene_donor = int(not current_gene_donor)
                new_genotype[chromosome_index] += parents[current_gene_donor].genotype[chromosome_index][allel_index]

        else:
            if parents[0].chromosome_fitnesses[chromosome_index] > parents[1].chromosome_fitnesses[chromosome_index]:
                new_genotype[chromosome_index] = parents[0].genotype[chromosome_index]
            else:
                new_genotype[chromosome_index] = parents[1].genotype[chromosome_index]

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

"""
--------------------------------- The real magic ------------------------------
"""

population = [Melody(create_random_genotype(), 0) for i in range(population_size)]
for generation in range(1, number_of_generations):

    new_population = []
    new_population.extend(elite(population))
    
    for i in range(population_size - elite_selection):
        parents = select_parents(population)
        new_individual = crossover(parents, generation)
        fitness(new_individual)
        new_individual = mutation(new_individual)
        new_population.append(new_individual)
    population = new_population

fitnesses = [individual.fitness for individual in population]

print(sum(fitnesses)/len(fitnesses), max(fitnesses))




