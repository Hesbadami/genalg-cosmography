import numpy as np
from time import time
from genetics import Genetics

data = np.genfromtxt('mock_pantheon.txt')
z1 = data[:, 0]
muu = data[:, 1]
error = data[:, 2]

population = 50
max_iter = 800
pb = 0.80
pm = 0.5
min_fittness = 0

a = time()
x = Genetics(
    z=z1,
    error=error,
    population=population,
    max_iter=max_iter,
    pb=pb,
    pm=pm,
    min_fittness=min_fittness
)


while not x.terminate():
    print("Gen", "\tBest", "\t\t\tAvg")
    print(
        x.generation, "\t"+str(x.best_fittness[-1]),
        "\t"+str(x.avg_fittness[-1])
    )
    print("Best answer:", x.final_ans.get_param())
    x.next_gen()

b = time()
print("Time:", round(b-a, 2), "seconds")
print(x.final_ans.get_param())
