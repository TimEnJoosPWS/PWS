from random import randint

for k in range(5):
	totalitems = 0
	failed = 0
	board = [["" for i in range(7)] for x in range(7)]
	solutions = []
	while totalitems - failed < 8:
		randX = randint(0,9)
		randY = randint(0,9)
		board[randY][randX] = "Q" if not board[randY][randX] == "Q" else failed += 1
		totalitems += 1
	solutions[k] = board