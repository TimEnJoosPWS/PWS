# -*- coding: utf-8 -*-


import sqlite3
import xlsxwriter

conn = sqlite3.connect('knapsack_data_3.0.db')

"""

knapsack example:

id (PRIMARY INT)      genotype (TEXT)    run    fitness (INT)     parent_0 (INT)   parent_1 (INT)    generation (INT)

0                       '0000000000'     0       0                                                    0
34                      '1111111111'     0       -133                                                 0
164                     '1110001001'     0       21                    0               34             1

knapsack_parameters example:

run_id (PRIMARY INT)    population_size (INT)   number_of_generations (INT)     mutation_rate (FLOAT) elite_selection (INT) crossover_type (TEXT)    crossover_points (INT)

0                       100                     100                             0.02                    5                   'universal_crossover'  
1                       100                     100                             0.02                    5                   'n_points_crossover'       1
9                       50                      200                             0.00                    3                   'n_points_crossover'       3


used queries:

conn.execute('''CREATE TABLE knapsack 
            (id INT PRIMARY KEY,
            genotype TEXT,
            fitness INT,
            parent_0 INT,
            parent_1 INT)''')

conn.execute('''ALTER TABLE knapsack ADD COLUMN generation INT''')
conn.execute('''ALTER TABLE knapsack ADD COLUMN run INT''')

conn.execute('''CREATE TABLE knapsack_parameters 
            (run_id INT PRIMARY KEY,
            population_size INT,
            number_of_generations INT,
            mutation_rate FLOAT,
            elite_selection INT
            )''')

conn.execute('''ALTER TABLE knapsack_parameters ADD COLUMN crossover_type TEXT''')
conn.execute('''ALTER TABLE knapsack_parameters ADD COLUMN crossover_points INT''')

stuff = conn.execute('''SELECT * FROM knapsack_parameters''')
for thing in stuff:
    print(thing[0])
    
stuff = conn.execute("DELETE FROM knapsack_parameters")
stuff = conn.execute("VACUUM")
stuff = conn.execute("DELETE FROM knapsack")
stuff = conn.execute("VACUUM")
conn.commit()

stuff = conn.execute("SELECT COUNT(*) FROM knapsack")
for thing in stuff:
    print(thing[0])


workbook = xlsxwriter.Workbook('knapsack_data.xlsx')

worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "id")
worksheet.write(0, 1, "genotype")
worksheet.write(0, 2, "fitness")
worksheet.write(0, 3, "parent_0")
worksheet.write(0, 4, "parent_1")
worksheet.write(0, 5, "generation")
worksheet.write(0, 6, "runs")




row = 1
data = conn.execute("SELECT * FROM knapsack")

for data_row in data:
    for col in range(7):
        worksheet.write(row, col, data_row[col])

    #worksheet.write(row, 1, data_row[0])
    row += 1

outfile = open("crossover_data.txt", "a+")

data = conn.execute("SELECT ks.run,  AVG(ks.fitness/(MAX(ks1.fitness/1.0, ks2.fitness/1.0))) FROM knapsack AS ks \
                         JOIN knapsack AS ks1 ON ks.parent_0 IS ks1.id\
                         JOIN knapsack as ks2 ON ks.parent_1 IS ks2.id\
                         WHERE ks.generation IS NOT 0\
                         AND ks.fitness > 0\
                         GROUP BY ks.run")

for line in data:
    outfile.write(str(line) + "\n")

outfile.close()

workbook = xlsxwriter.Workbook('knapsack_data.xlsx')

worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "id")
worksheet.write(0, 1, "genotype")
worksheet.write(0, 2, "fitness")
worksheet.write(0, 3, "parent_0")
worksheet.write(0, 4, "parent_1")
worksheet.write(0, 5, "generation")
worksheet.write(0, 6, "runs")




row = 1
data = conn.execute("SELECT * FROM knapsack")

for data_row in data:
    for col in range(7):
        worksheet.write(row, col, data_row[col])

    #worksheet.write(row, 1, data_row[0])
    row += 1

outfile = open("crossover_data.txt", "a+")

data = conn.execute("SELECT kp.crossover_type, kp.crossover_points, ks.run,  AVG(ks.fitness/(MAX(ks1.fitness/1.0, ks2.fitness/1.0))) FROM knapsack AS ks \
                         JOIN knapsack AS ks1 ON ks.parent_0 IS ks1.id\
                         JOIN knapsack as ks2 ON ks.parent_1 IS ks2.id\
                         JOIN knapsack_parameters AS kp ON ks.run IS kp.run_id\
                         WHERE ks.generation IS NOT 0\
                         AND ks.fitness/(MAX(ks1.fitness/1.0, ks2.fitness/1.0)) > 0\
                         GROUP BY ks.run")

for line in data:
    outfile.write(str(line) + "\n")

outfile.close()
stuff = conn.execute("DELETE FROM knapsack_parameters")
stuff = conn.execute("VACUUM")
stuff = conn.execute("DELETE FROM knapsack")
stuff = conn.execute("VACUUM")


import knapsack
data = conn.execute("SELECT COUNT(*) FROM knapsack_parameters")
for i in data:
    print(i[0])



"""




conn.close()