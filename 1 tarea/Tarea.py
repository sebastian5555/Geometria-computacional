from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
from sympy import *
import matplotlib.patches as mpatches
import networkx as nx


class TIN:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.points = [(X[i], Y[i], Z[i]) for i in range(len(self.X))]
        self.tri = Delaunay(np.array([[x, y] for x, y in zip(self.X, self.Y)]))

    # Funcion primer punto
    def plot_surface(self):

        # Triangulacion
        plt.triplot(self.X, self.Y, self.tri.simplices)
        plt.title("Delauney triangulation")
        plt.show()

        # Superficie
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1,  projection='3d')
        surf = ax.plot_trisurf(
            self.X, self.Y, self.Z,
            triangles=self.tri.simplices,
            cmap=plt.get_cmap('hot'),
            linewidth=0.2,
            antialiased=True,
            edgecolor='grey',
        )
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        ax.set_title('Elevation profile')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()

    # Funcion segundo punto
    def interpolation(self, points):

        # Simplejo en donde se encuentra el punto
        simplejo = self.tri.find_simplex(points)

        # Separa el simplejo por puntos
        p1 = np.array(self.points[self.tri.simplices[simplejo][0]])
        p2 = np.array(self.points[self.tri.simplices[simplejo][1]])
        p3 = np.array(self.points[self.tri.simplices[simplejo][2]])

        # Ecuacion del plano con 3 puntos
        v1 = p3 - p1
        v2 = p2 - p1
        cp = np.cross(v1, v2)
        a, b, c = cp
        d = np.dot(cp, p3)
        z = Symbol('z')
        x = points[0]
        y = points[1]
        ecuacion = a*x + b*y + c*z - d
        ecuacion = tuple(solve(ecuacion, z))
        print("INTERPOLATION: ")
        print("La altura del punto {0} es {1}".format(points, ecuacion))
        print('\n')

        # Coordenadas del simplejo
        px = [p1[0], p2[0], p3[0], points[0]]
        py = [p1[1], p2[1], p3[1], points[1]]
        pz = [p1[2], p2[2], p3[2], float(ecuacion[0])]

        # grafica
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1,  projection='3d')
        tri2 = Delaunay(np.array([[x, y] for x, y in zip(px, py)]))
        ax.scatter(px[:3], py[:3], pz[:3], color='blue', alpha=1)
        ax.scatter(px[3], py[3], pz[3], color='black', alpha=1)
        ax.plot_trisurf(
            self.X, self.Y, self.Z,
            alpha=0.3,
            color='silver',
            linewidth=0.01,
            antialiased=False,
        )
        ax.plot_trisurf(
            px, py, pz, triangles=tri2.simplices,
            alpha=1,
            color='red',
            linewidth=0.01,
            antialiased=False,
            edgecolor='darkorange',
        )
        ax.set_title('Elevation value', loc='right')
        green_patch = mpatches.Patch(color='blue', label="Puntos del simplejo")
        black_patch = mpatches.Patch(color='black', label="Punto interpolado")
        red_patch = mpatches.Patch(color='red', label='Area del simplejo')
        ax.legend(
            handles=[green_patch, black_patch, red_patch],
            loc='upper left'
        )
        plt.show()

    # Funcion tercer punto
    def peak_point(self):

        # Maximos relativos
        L_vecinos = []
        water_source = []
        for i in range(len(self.X)):
            L_vecinos = [self.tri.vertex_neighbor_vertices[1]
                         [self.tri.vertex_neighbor_vertices[0]
                          [i]:self.tri.vertex_neighbor_vertices[0][i+1]]]
            contador = 0
            for k in L_vecinos:
                for j in k:
                    if self.Z[i] >= self.Z[j]:
                        contador = contador + 1
                if contador == len(k):
                    water_source.append(i)

        # Puntos peak
        px = [self.X[x] for x in water_source]
        py = [self.Y[x] for x in water_source]
        pz = [self.Z[x] for x in water_source]
        points = [(px[i], py[i], pz[i]) for i in range(len(px))]
        print("WATER SOURCE")
        for i in range(len(points)):
            print("Peak point: " + str(points[i]))
        print('\n')

        # Grafica
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1,  projection='3d')
        ax.scatter(px, py, pz, alpha=1, color='red', marker='o')
        ax.plot_trisurf(
            self.X, self.Y, self.Z,
            alpha=0.3,
            triangles=self.tri.simplices,
            color='white',
            linewidth=0.01,
            antialiased=False,
            edgecolor='white',
        )
        ax.legend(['Peak points'])
        ax.set_title('Water sources')
        plt.show()

    # Funcion cuarto punto
    def anti_peak_point(self):

        # Minimos relativos
        L_vecinos = []
        water_source = []
        for i in range(len(self.X)):
            L_vecinos = [self.tri.vertex_neighbor_vertices[1]
                         [self.tri.vertex_neighbor_vertices[0]
                          [i]:self.tri.vertex_neighbor_vertices[0][i+1]]]
            contador = 0
            for k in L_vecinos:
                for j in k:
                    if self.Z[i] <= self.Z[j]:
                        contador = contador + 1
                if contador == len(k):
                    water_source.append(i)

        # Puntos anti peak
        px = [self.X[x] for x in water_source]
        py = [self.Y[x] for x in water_source]
        pz = [self.Z[x] for x in water_source]
        points = [(px[i], py[i], pz[i]) for i in range(len(px))]
        print('WATER PIT')
        for i in range(len(points)):
            print("Anti peak point: " + str(points[i]))
        print('\n')

        # Grafica
        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1,  projection='3d')
        ax.scatter(px, py, pz, alpha=1, color='blue', marker='o')
        ax.plot_trisurf(
            self.X, self.Y, self.Z,
            alpha=0.3,
            triangles=self.tri.simplices,
            color='white',
            linewidth=0.01,
            antialiased=False,
            edgecolor='white'
        )
        ax.legend(['Anti peak points'])
        ax.set_title('Water pit')
        plt.show()

    # Funcion quinto punto
    def dual_graph(self):

        G = nx.Graph()
        puntos = [(self.X[i], self.Y[i]) for i in range(len(self.X))]

        # Vertices
        for i in puntos:
            simplejo = self.tri.find_simplex(i)
            p1 = np.array(self.points[self.tri.simplices[simplejo][0]])
            p2 = np.array(self.points[self.tri.simplices[simplejo][1]])
            p3 = np.array(self.points[self.tri.simplices[simplejo][2]])
            puntomedio = (
                (sum([p1[0], p2[0]], p3[0]))/3,
                (sum([p1[1], p2[1]], p3[1]))/3
            )
            pos = (puntomedio[0], puntomedio[1])
            G.add_node(i, pos=pos)
        # Superficie con vertices de grafo dual
        pos2 = nx.get_node_attributes(G, 'pos')
        plt.triplot(self.X, self.Y, self.tri.simplices)
        nx.draw(G, pos=pos2, node_size=10, node_color='red')
        plt.title(' Superficie con vertices del grafo dual ')
        plt.show()
