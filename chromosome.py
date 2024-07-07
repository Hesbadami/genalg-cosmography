import random
import numpy as np
from scipy.integrate import quad

data = np.genfromtxt('mock_pantheon.txt')
z1 = data[:, 0]
muu = data[:, 1]
error = data[:, 2]


def E(z, param):
    H1 = 1 + param[0]
    H2 = -pow(param[0], 2) + param[1]
    H3 = 3*pow(param[0], 2)*(1+param[0]) - param[1]*(3+4*param[0]) - param[2]
    H4 = -3*pow(param[0], 2)*(4+8*param[0]+5*pow(param[0], 2))
    + param[1]*(12+32*param[0]+25*pow(param[0], 2)-4*param[1])
    + param[2]*(8+7*param[0]) + param[3]

    Q1 = (-6*H1*H4 + 12*H2*H3)/(24*H1*H3 - 36*H2**2)
    Q2 = (3*H2*H4 - 4*H3**2)/(24*H1*H3 - 36*H2**2)
    P0 = 1
    P1 = H1 + Q1
    P2 = H2/2 + Q1*H1 + Q2

    EE = (P0 + P1*z + P2*z**2)/(1 + Q1*z + Q2*z**2)
    return 1/EE


def mu(z, param):
    muu = 5*np.log10((1+z)*quad(E, 0, z, args=param)[0])
    return muu

class Chromosome:
    def __init__(self, param=None):
        self.param = param
        if self.param is None:
            self.param = [
                random.uniform(-10, 0),
                random.uniform(0, 20),
                random.uniform(-20, 20),
                random.uniform(-15, 30)
            ]

    def xi2(self, z, error):
        A= 0
        B= 0
        C= 0
        for i in range(len(z)):
            A+= pow(mu(z[i], self.param)-muu[i], 2)/pow(error[i], 2)
            B+= (mu(z[i], self.param)-muu[i])/pow(error[i], 2)
            C+= 1/pow(error[i], 2)
            x2= A- pow(B,2)/C
        return x2

    def get_param(self):
        return self.param

    def fittness(self, z, error):
        self.ft = np.abs(1044 - self.xi2(z, error))
        return self.ft

    def mutate(self, ranges, active, possibility=0.005):
        for i in range(4):
            if (i in active) and (possibility >= random.randint(0, 1000)/1000):
                k = random.uniform(-2, 2)
                self.param[i] += random.uniform(ranges[i][0]*k, ranges[i][1]*k)

    def breed(self, mate, active):
        origin = [self, mate]

        child1 = Chromosome([
            origin[random.randint(0, 1)].get_param()[0],
            origin[random.randint(0, 1)].get_param()[1],
            origin[random.randint(0, 1)].get_param()[2],
            origin[random.randint(0, 1)].get_param()[3],
        ])

        child2 = Chromosome([
            origin[random.randint(0, 1)].get_param()[0],
            origin[random.randint(0, 1)].get_param()[1],
            origin[random.randint(0, 1)].get_param()[2],
            origin[random.randint(0, 1)].get_param()[3],
        ])

        #child1 = Chromosome([
        #    (np.mean((self.get_param()[i], mate.get_param()[i]))) if i in active else self.get_param()[i] for i in range(4)
        #])

        #child2 = Chromosome([
        #    (np.mean((self.get_param()[i], mate.get_param()[i]))) if i in active else mate.get_param()[i] for i in range(4)
        #])

        return child1, child2
