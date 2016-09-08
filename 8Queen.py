from random import randint

for k in range(5):
	totalitems = 0
	failed = 0
	board = [["" for i in range(8)] for x in range(8)]
	solutions = []
	while totalitems - failed <= 8:
		randX = randint(0,8)
		randY = randint(0,8)
		board[randY][randX] = "Q" if not board[randY][randX] == "Q" else failed += 1
		totalitems += 1
	solutions[k] = board
