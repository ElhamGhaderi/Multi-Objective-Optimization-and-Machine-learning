import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from itertools import combinations
from random import sample, uniform
import pandas as pd
from time import sleep
import os

# df1 = pd.DataFrame([1.00,12.0,32.21])
# df1.head()
# t = df1.iloc[:,0:1]
# t1 = t.to_numpy()

nGene = 13
geneMin = np.array([.08,0.00,0.00,0.00,0.00,0.00,0.00,4,0,0.30,12.00,0.30,5.00])
geneMax = np.array([.92,1.00,1.00,1.00,1.00,1.00,1.00,10,1000,1.00,20.00,1.00,12.00])

nObjectives = 3

nGeneration = 100

population_size = 100

nCrossover = 70
nMutation = 20

# blend crossover hyper-parameter
alpha = 0.5

# mutation hyperparameter
beta = 10

results = pd.DataFrame(columns=['ParameterP','Point1X','Point1Y','Point2X','Point2Y','Point3X', 'Point3Y', 'Number','Seed','ColumnsThikness','ColumnsDiameter','ElementsThikness','ElementsDiameter','Mass','Displacement','ElasticEnergy'])

def cost(x):

    df1 = pd.DataFrame(x)

    df1.to_csv('inputs.csv')
    sleep(15)
    df2 = pd.read_csv('output.csv')


    t = df1.iloc[:,0:1]
    t1 = t.to_numpy()
    t2 = t1.reshape(-1,)
    t3 = list(t2)

    h = df2.iloc[:,0:1]
    h1 = h.to_numpy()
    h2 = h1.reshape(-1,)
    h3 = list(h2)

    results.loc[len(results.index)] = t3 + h3

    h4 = np.array(h3)

    return h4

class Agent:
    _temp = []
    _pop = []

    def __init__(self, genome=None):
        if genome:
            self.genome = np.array(genome)
        else:
            self.genome = np.array([uniform(i,j) for i,j in zip(geneMin,geneMax)])

        Agent._temp.append(self)


        self.fitness = cost(self.genome)

        Agent._pop += Agent._temp
        Agent._temp = []





    @classmethod
    def non_dominated_sorting(cls):
        c = 1
        nds = {f'front{c}':[]}
        n = len(cls._pop)

        for i in cls._pop:
            # each object receives three new attributes
            # domination list, dominated count, rank
            i.domination_list = []
            i.dominated_count = 0
            i.rank = None

        for i,j in combinations(range(n),2):
            data1 = cls._pop[i]
            data2 = cls._pop[j]

            if all(data1.fitness <= data2.fitness) & any(data1.fitness < data2.fitness):
                # it means that data1 is dominating data2
                data1.domination_list.append(j)
                data2.dominated_count += 1
            elif all(data2.fitness <= data1.fitness) & any(data2.fitness < data1.fitness):
                # it means that data2 is dominating data1
                data2.domination_list.append(i)
                data1.dominated_count += 1

        for i in range(n):
            if cls._pop[i].dominated_count == 0:
                nds[f'front{c}'].append(i)
                cls._pop[i].rank = c

        while True:
            c += 1
            nds[f'front{c}'] = []
            for i in nds[f'front{c-1}']:
                data1 = cls._pop[i]
                for j in data1.domination_list:
                    data2 = cls._pop[j]
                    data2.dominated_count -= 1
                    if data2.dominated_count == 0:
                        nds[f'front{c}'].append(j)
                        data2.rank = c

            if len(nds[f'front{c}'])==0:
                del nds[f'front{c}']
                break

        return nds

    @classmethod
    def cd(cls,fronts):
        # generate a new instance attribute for crowding distance value
        for i in cls._pop:
            i.crowding_distance = None

        for front in fronts.values():
            n = len(front)

            if n>1:
                costs = np.vstack([cls._pop[k].fitness for k in front])
                d = np.zeros((n, nObjectives))


                for j in range(nObjectives):
                    c = np.sort(costs[:,j])
                    idx = np.argsort(costs[:,j])

                    # the first and last items in a front have inf crowding distance
                    d[idx[0]][j] = np.inf
                    d[idx[-1]][j] = np.inf

                    for i in range(1,n-1):
                        d[idx[i]][j] = np.abs(c[i+1]-c[i-1]) / np.abs(c[0] - c[-1])

                for i,j in enumerate(front):
                    cls._pop[j].crowding_distance = np.sum(d[i,:])

            else:
                cls._pop[front[0]].crowding_distance = np.inf







