from random import randint

def createSolution():
	totalitems = 0
	failed = 0
	board = [["" for i in range(8)] for x in range(8)]
	solutions = []
	while totalitems - failed <= 8:
		randX = randint(0,8)
		randY = randint(0,8)
		board[randY][randX] = "Q" if not board[randY][randX] == "Q" else failed += 1
		totalitems += 1
	return board

solutions = []
for i in range(10):
	solutions[i] = createSolution()

fitnesses = []
def fitness_count():
	for i in solutions:
		if sum(x.count('Q') for x in solutions[i]) == 8:
			fitnesses[i] = 100
		else:
			fitnesses[i] = 10
	return fitnesses

	
