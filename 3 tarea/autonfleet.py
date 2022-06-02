from traceback import print_tb
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
from scipy.spatial import distance


class AutonFleet:

    def __init__(self, Fleet):
        # Proa
        self.bow = np.array([
            [Fleet[i][1], Fleet[i][3]]
            for i in range(len(Fleet))
            ])
        # Popa
        self.stern = np.array([
            [Fleet[i][0], Fleet[i][2]]
            for i in range(len(Fleet))
            ])
        # Ubicacion(punto medio(bow,stern))
        self.location = np.array([
            [
                (self.bow[i][0] + self.stern[i][0])/2,
                (self.bow[i][1] + self.stern[i][1])/2
            ]
            for i in range(len(self.bow))
            ])
        # kdtree ubicaciones
        self.kdtree_locations = KDTree(self.location)
        # kdtree segmentos
        self.kdtree_segments = KDTree(Fleet)

    # Grafica la flota
    def plot_fleet(self, color, opacity):
        for i in range(len(self.stern)):
            x = []
            y = []
            x.append(self.bow[i][0])
            x.append(self.stern[i][0])
            y.append(self.bow[i][1])
            y.append(self.stern[i][1])
            p_fleet, = plt.plot(x, y, color, alpha=opacity)
        p_fleet.set_label('Fleet')

    # 1 punto
    def nearest_ships(self, vessel, s):
        neighbours = []
        distances, neighbours = self.kdtree_locations.query(vessel, s, p=2)

        # Punto con sus vecinos
        print("PUNTO 1")
        print("Vessel: {0}".format(vessel))
        cont = 1
        for i in neighbours:
            print("Neighbour {0}: ({1},{2})".format(
                cont,
                self.kdtree_locations.data[i, 0],
                self.kdtree_locations.data[i, 1])
                )
            cont = cont + 1

        # Graficas
        # Flota
        self.plot_fleet('r', 1)
        # Buque
        p_vessel = plt.scatter(
            vessel[0],
            vessel[1],
            marker="*",
            s=20,
            color="blue",
            alpha=1
            )
        p_vessel.set_label('Vessel')
        # Buques vecinos
        for i in neighbours:
            p_neighbours = plt.scatter(
                self.kdtree_locations.data[i, 0],
                self.kdtree_locations.data[i, 1],
                marker="*",
                s=20,
                color="black",
                alpha=1
            )
        p_neighbours.set_label('{0} closest ships'.format(s))

        plt.legend()
        plt.title("Nearest ships")
        plt.show()

    # 2 punto
    def avoiding_collisions(self, index_center, radius):
        center = self.kdtree_segments.data[index_center]
        ball_neighbours = self.kdtree_segments.query_ball_point(
            center,
            radius,
            p=np.inf
            )

        cont = 0
        # Eliminando vecinos redundantes
        for i in ball_neighbours:
            if distance.euclidean(
                self.kdtree_locations.data[index_center],
                self.kdtree_locations.data[i]
            ) >= radius:
                ball_neighbours.pop(cont)
                cont = cont + 1

        print("PUNTO 2")
        print("Vessel: {0}".format(center))
        for i in ball_neighbours:
            print("Within ball : {0}".format(
                self.kdtree_segments.data[i])
            )

        # Flota
        self.plot_fleet('k', 1)

        # Dentro del circulo
        for i in ball_neighbours:
            x = []
            y = []
            x.append(self.kdtree_segments.data[i, 0])
            x.append(self.kdtree_segments.data[i, 1])
            y.append(self.kdtree_segments.data[i, 2])
            y.append(self.kdtree_segments.data[i, 3])
            p_fleet, = plt.plot(x, y, 'r', alpha=1)
        p_fleet.set_label('Within circle')

        # Centro del circulo
        plt.plot(center[0:2], center[2:4], 'b', alpha=1, label='Centered ship')

        # Circulo
        draw_circle = plt.Circle(
            (self.kdtree_locations.data[index_center]),
            radius,
            color='g',
            fill=False
            )
        plt.gcf().gca().add_artist(draw_circle)

        plt.xlim([-0.3, 1.3])
        plt.ylim([-0.3, 1.3])
        plt.title("Avoiding collisions")
        plt.legend()
        plt.show()

    # 3 punto
    def partner_lookup(self):
        closest_pair = []

        # Vecino mas cercano
        for i in range(len(self.kdtree_locations.data)):
            distances, neighbour = self.kdtree_locations.query(
                self.kdtree_locations.data[i],
                2,
                p=2
                )
            closest_pair.append([
                self.kdtree_locations.data[i],
                self.kdtree_locations.data[neighbour[1]],
                i,
                neighbour[1]
                ])

        # Punto con su par mas cercano
        print("PUNTO 3")
        plot_closest = []
        for i in range(len(closest_pair)):
            print("Vessel: {0} - Closest pair: {1}".format(
                closest_pair[i][0],
                closest_pair[i][1])
                )

        # Plot par mas cercano
        for i in range(len(closest_pair)):
            x = []
            y = []
            x.append(self.kdtree_locations.data[i][0])
            x.append(self.kdtree_locations.data[closest_pair[i][3]][0])
            y.append(self.kdtree_locations.data[i][1])
            y.append(self.kdtree_locations.data[closest_pair[i][3]][1])
            p_closest, = plt.plot(x, y, '--', color='k', alpha=0.8)
        p_closest.set_label('Closest pair')

        # Plot flota
        self.plot_fleet('r', 1)

        plt.legend()
        plt.title("Partner lookup")
        plt.show()

    # 4 punto
    def operation_radius(self):
        x = 0
        y = 0
        dist = []

        # Centro
        for i in range(len(self.kdtree_segments.data)):
            x = x + self.kdtree_locations.data[i][0]
            y = y + self.kdtree_locations.data[i][1]

        x = x/len(self.kdtree_locations.data)
        y = y/len(self.kdtree_locations.data)

        # Radio
        for i in range(len(self.kdtree_segments.data)):
            dist.append(distance.euclidean(self.bow[i], (x, y)))
            dist.append(distance.euclidean(self.stern[i], (x, y)))
        r = (max(dist)) + 0.01

        print("PUNTO 4")
        print("Radius of the circle: {0}".format(r))

        # Plot flota
        self.plot_fleet('r', 1)

        # Plot circulo
        draw_circle = plt.Circle(
            (x, y),
            r,
            color='k',
            fill=False
            )
        plt.gcf().gca().add_artist(draw_circle)
        draw_circle.set_label("Circle")

        plt.xlim([-0.3, 1.3])
        plt.ylim([-0.3, 1.3])
        plt.title("Operation radius")
        plt.legend(fontsize=8.5)
        plt.show()
