# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 19:50:35 2017
"""

from random import random, randint

crossover_chance = 0.3


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
            crossover_point = randint(0, len(length_chromosome))
            current_gene_donor = randint(0, 1)

            for allel_index in len(length_chromosome):
                if allel_index == crossover_point:
                    current_gene_donor = int(not current_gene_donor)
                new_genotype[chromosome_index] += parents[current_gene_donor].genotype[chromosome_index][allel_index]

        else:
            if parents[0].chromosome_fitnesses[chromosome_index] > parents[1].chromosome_fitnesses[chromosome_index]:
                new_genotype[chromosome_index] = parents[0].genotype[chromosome_index]
    return Melody(new_genotype)
