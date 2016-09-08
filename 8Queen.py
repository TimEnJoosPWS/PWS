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

	# fitness function, gebaseerd op hoeveel aanvallende koninginnenparen er zijn

fitnesses = []
total_row_fitness = []
total_colom_fitness = []
total_diagonal_fitness = []

def fitness_count(solutions):
	for i in solutions:
		for j in solutions[i]:
			row_queens = len(solutions[i][j]) 							# berekent de queens op een rij
			row_fitness[j] = ((row_queens - 1) * row_queens) / 2  		# berekent de fitnesswaarde van de rij met index j
		total_row_fitness[i] = sum(row_fitness) 						# totale rij-fitheid van het i-de bord is de som van 8 aparte fitnesswaarden (waarbij een lager fitheidsgetal een hogere fitheid betekent)

		for j in solutions[i]:		# geen idee of ik het volgende handig heb gedaan, maar het was best lastig om per kolom de koninginnen te vinden.
			colom_queens = 0
			for k in solutions[i][j]:
				if solutions[i][k][j] == "Q":
					colom_queens += 1
			colom_fitness[j] = ((colom_queens - 1) * colom_queens) / 2
		total_colom_fitness[i] = sum(colom_fitness)

# nu de diagonalen nog. Hier moet je volgens mij NumPy voor gebruiken.


	
