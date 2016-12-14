# -*- coding: utf-8 -*-
import sqlite3
import matplotlib.pyplot as plt


def generate_data(crossover_type, crossover_points):
    conn = sqlite3.connect('knapsack_data_3.0.db')
    query = "SELECT COUNT(DISTINCT run) FROM knapsack\
                JOIN knapsack_parameters AS kp\
                ON kp.run_id = run\
                WHERE fitness = 102\
                AND kp.crossover_type = '%s'\
                AND kp.crossover_points = %f\
                GROUP BY generation" % (crossover_type, crossover_points)
    raw_data = conn.execute(query)
    result = [y[0] for y in raw_data]
    print(len(result))
    conn.close()
    return result

fig = plt.figure()
fig.suptitle('Variatie in de populatie over de generaties', fontsize=14,
             fontweight='bold')

plt.plot([x for x in range(100)], generate_data("universal_crossover", 0),
         label='Universele crossover')
plt.plot([x for x in range(99)], generate_data("n_points_crossover", 1),
         label='1-punts crossover')
plt.plot([x for x in range(100)], generate_data("n_points_crossover", 2),
         label='2-punts crossover')

ax = fig.add_subplot(111)
ax.set_xlabel("Generaties")
ax.set_ylabel("Aantal verschillende individuen in de populatie")
plt.legend(loc='upper right')
plt.show()

"""
-------------- GEBRUIKTE QUERIES VOOR HET GENEREREN VAN DATA ------------------

Unieke genotypen:

"SELECT AVG(variation) FROM\
                (SELECT ks.run, ks.generation, COUNT(DISTINCT genotype)\
                     AS variation FROM knapsack AS ks\
                JOIN knapsack_parameters AS kp ON ks.run IS kp.run_id\
                WHERE kp.crossover_type IS '%s' AND\
                   kp.crossover_points IS %f\
                GROUP BY generation, run)\
            GROUP BY generation;" % (crossover_type, crossover_points)

Gemiddelde fitness:

"SELECT AVG(fitness) FROM knapsack AS ks  \
                     JOIN knapsack_parameters AS kp ON ks.run IS kp.run_id\
                     WHERE kp.crossover_type IS 'crossover_type'\
                     AND kp.crossover_points IS crossover_points\
                     GROUP BY generation" % (crossover_type, crossover_points)

Max fitnesses:
"SELECT generation, MAX(fitness) FROM knapsack\
             WHERE run IS %d GROUP BY generation ;"%(run)
"""
