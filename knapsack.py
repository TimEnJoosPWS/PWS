from random import *

    # initiation

n = 8
def createSolution():
    decimal_solution = randint(0, 2**n - 1)
    binary_solution = str(bin(decimal_solution)[2:])
    solution = (n - len(binary_solution)) * '0' + binary_solution
    return solution
