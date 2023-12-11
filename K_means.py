import pandas as pd
import numpy as np
from random import random, uniform
from math import sqrt

class Kmeans(object):
    def __init__(self, data: pd.DataFrame, k: int, normalize = False):
        self.k = k
        self.data = data
        self.columns = self.data.columns
        self.X = pd.DataFrame(self.data)
        self.trained = False

        ranges = []
        for column in self.X.columns:
            ranges.append([self.X[column].min(), self.X[column].max()])

        self.centroides = [[uniform(ranges[j][0], ranges[j][1]) for j in range(len(self.columns))] for i in range(self.k)]
        if normalize:
            self.normalize()

    def train(self, iterations: int):
        self.X["cluster"] = None

        for iteration in range(iterations):
            
            print(iter)
            centroides_nuevos = [[0 for j in range(len(self.columns))] for i in range(self.k)]
            elementos_cluster = [0 for i in range(self.k)]
            clusters = []

            for index, row in self.X.iterrows():
                r = list(row[self.columns])
                dist_a_centroides = [self.squared_euclidean_norm(r, centroide) for centroide in self.centroides]
                k = self.get_min_index(dist_a_centroides)
                centroides_nuevos[k] = self.sum_vectors(centroides_nuevos[k], r)
                elementos_cluster[k] += 1
                clusters.append(k)

            self.X["cluster"] = pd.Series(clusters)
            centroides_nuevos = [self.divide_by_number(centroides_nuevos[i], elementos_cluster[i], i) for i in range(self.k)]
            
            if centroides_nuevos == self.centroides:
                print(f"Convergencia alcanzada en la iteracion numero: {iteration}")
                break

            self.centroides = centroides_nuevos

        self.trained = True

    def get_cluster(self, data):
        if not self.trained:
            print("Debe entrenar primero antes de evaluar datos")

        cluster = 0

        distances = [self.squared_euclidean_norm(data, centroide) for centroide in self.centroides]

        for i in range(len(distances)):
            if distances[i] < distances[cluster]:
                cluster = i

        return cluster

    def divide_by_number(self, vector: list, divisor: int, i: int):
        new_vector = [0 for i in range(len(vector))]
        
        if (divisor == 0):
            return self.centroides[i]

        for i in range(len(vector)):
            new_vector[i] = vector[i] / divisor

        return new_vector

    def get_min_index(self, lista: list):
        index = 0
        for i in range(len(lista)):
            if lista[i] < lista[index]:
                index = i


        return index

    def squared_euclidean_norm(self, v1, v2) -> float:
        
        if (len(v1) != len(v2)):
            print("Error de dimensiones de los vectores")
            return

        suma = 0
        for i in range(len(v1)):
            suma = suma + ((v1[i]-v2[i])**2)

        return suma
    
    def euclidean_norm(self, v1, v2) -> float:
        return sqrt(self.squared_euclidean_norm(v1,v2))

    def sum_vectors(self, v1, v2):
        if (len(v1) != len(v2)):
            print("Error de dimensiones de los vectores")
            return

        res = [0 for i in range(len(v1))]

        for i in range(len(v1)):
            res[i] = v1[i]+v2[i]

        return res
    
    def normalize(self):
        for column in self.columns:
            mn = self.X[column].min()
            mx = self.X[column].max()
            self.X[column] = self.X[column].map(lambda x: (x - mn) / (mx - mn))

    def inertia(self):
        inertia = 0
        for i in range(self.k):
            elementos_cluster = self.X[self.X['cluster'] == i]
            elementos_cluster = elementos_cluster[self.columns]
            for _, row in elementos_cluster.iterrows():
                inertia += self.squared_euclidean_norm(self.centroides[i], list(row))

        return inertia