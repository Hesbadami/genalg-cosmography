import warnings
import random
from chromosome import Chromosome
ok = "[ \033[1m\033[92m OK \033[0m\033[0m ]"
fail = "[\033[1m\033[91mFAILED\033[0m\033[0m]"

class Genetics:
    def __init__(
        self,
        z,  # data points z
        error,  # data points error
        population=1000,  # population
        max_iter=800,  # max number of generations
        pb=0.80,  # breeding probability
        pm=0.005,  # mutation probability
        min_fittness=0
    ):

        self.z = z
        self.error = error

        self.generation = 1
        self.population_count = population
        self.max_iter = max_iter
        self.pb = pb
        self.pm = pm
        self.min_fittness = min_fittness

        self.avg_fittness = []  # stores average fittness value per generation
        self.best_fittness = []  # stores best fittness value per generation

        self.population = [Chromosome() for c in range(self.population_count)]
        print(ok, 'Generated initial population')

        self.fitt = []

        with warnings.catch_warnings():
            warnings.simplefilter('error')
            for p in range(self.population_count):
                first = True
                while True:
                    try:
                        self.fitt.append(self.population[p].fittness(self.z, self.error))
                        break
                    except:
                        if first:
                            print(fail, f'Chromosome {p} is corrupted, attempting replacement')
                            first = False
                        self.population[p] = Chromosome()

        print(ok, 'Calculated fittness value for all chromosomes')

        self.final_ans = self.population[0]
        self.final_ans_ft = self.fitt[0]

        self.save_stats()
        print(ok, 'Stats saved')

        self.active = [0]

    def save_stats(self):
        sigma = 0
        best = self.population[0]
        bf = self.fitt[0]
        for i in range(self.population_count):
            c = self.population[i]
            cf = self.fitt[i]
            sigma += cf
            if cf < bf:
                best = c
                bf = cf
        self.avg_fittness.append(sigma/self.population_count)
        self.best_fittness.append(bf)

        if self.final_ans_ft > bf:
            self.final_ans = best
            self.final_ans_ft = bf

    def select_parents(self):
        parents = [(i, self.fitt[i]) for i in range(self.population_count)]
        parents.sort(key=lambda a: a[1])
        parents = parents[:int(self.population_count/2)]
        parents = [self.population[p[0]] for p in parents]
        return parents*2

    def reproduce(self, parents):
        childes = []
        a = 0
        while a + 1 < len(parents):
            r = random.randint(0, self.population_count)
            if r >= self.pb * self.population_count:
                childes.append(Chromosome(parents[a].get_param()))
                childes.append(Chromosome(parents[a+1].get_param()))
            else:
                childes.extend(parents[a].breed(parents[a+1], self.active))
            a += 2
        return childes

    def next_gen(self):

        if self.generation%20 == 0:
            if self.active == [0]:
                self.active = [1]

            elif self.active == [1]:
                self.active = [2]

            elif self.active == [2]:
                self.active = [3]

            elif self.active == [3]:
                self.active = [0]

        parents = self.select_parents()
        print(ok, 'Parents selected')

        childes = self.reproduce(parents)
        print(ok, 'Offsprings created')

        qs = []
        js = []
        ss = []
        ls = []

        for c in childes:
            qs.append(c.get_param()[0])
            js.append(c.get_param()[1])
            ss.append(c.get_param()[2])
            ls.append(c.get_param()[3])

        ranges = [
            [min(qs), 0],
            [0, max(js)],
            [min(ss), max(ss)],
            [min(ls), max(ls)]
        ]
        print(ok, 'Mutation range calculated')

        self.fitt = []

        with warnings.catch_warnings():
            warnings.simplefilter('error')
            for c in range(self.population_count):
                first = True
                while True:
                    try:
                        temp = Chromosome(childes[c].get_param())
                        temp.mutate(ranges, self.active, possibility=self.pm)
                        self.fitt.append(temp.fittness(self.z, self.error))
                        childes[c] = Chromosome(temp.get_param())
                        break
                    except:
                        if first:
                            print(fail, f'Offspring {c} is corrupted, attempting mutation')
                            first = False
                        continue

        self.population = childes
        print(ok, 'New generation successfully generated')

        self.save_stats()
        print(ok, 'Stats saved')
        self.generation += 1

    def terminate(self):
        if self.min_fittness >= self.best_fittness[-1]:
            print(ok, 'Achieved optimal fittness value')
            return True

        return self.generation >= self.max_iter
