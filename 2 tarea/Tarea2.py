import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import ConvexHull
import matplotlib as mpl
import matplotlib.cm as cm
from scipy.spatial import distance


class FlightPlan:

    def __init__(self, borders, airports, airports_info):
        # Bordes Colombia
        self.borders = np.array([[x, y] for y, x in borders])
        # Voronoi
        self.voronoi = Voronoi(
            np.array([[x, y] for y, x in airports]),
            incremental=True
            )
        # Convex hull
        self.hull = ConvexHull(np.array([[x, y] for y, x in airports]))
        # Altura aeropuertos
        self.airport_elevation = [
            airports_info[i][0]
            for i in range(len(airports_info))
            ]
        # Nombre,ciudades aeropuertos
        self.airport_info = [
            airports_info[i][1:4]
            for i in range(len(airports_info))
            ]

    # 1 punto
    def plot_voronoi(self):

        # Escala de colores
        min_z = min(self.airport_elevation)
        max_z = max(self.airport_elevation)
        norm = mpl.colors.Normalize(vmin=min_z, vmax=max_z, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.YlGnBu)

        # Diagrama de Voronoi
        voronoi_plot_2d(
            self.voronoi,
            show_vertices=False,
            show_points=False,
            s=1
            )

        # Evitar area infinita
        self.voronoi.add_points([
            [-1000, 1000],
            [1000, -1000],
            [-1000, -1000],
            [1000, 1000]
            ])
        self.voronoi.close()

        # Relleno Voronoi
        for r in range(len(self.voronoi.point_region)):
            region = self.voronoi.regions[self.voronoi.point_region[r]]
            if -1 not in region:
                polygon = [self.voronoi.vertices[i] for i in region]
                plt.fill(
                    *zip(*polygon),
                    color=mapper.to_rgba(self.airport_elevation[r]),
                    alpha=1
                    )

        # Aeropuertos
        plt.scatter(
            self.voronoi.points[:, 0],
            self.voronoi.points[:, 1],
            marker="o",
            s=6,
            color="red",
            alpha=1
            )

        # Colombia
        plt.plot(self.borders[:, 0], self.borders[:, 1], 'k', alpha=0.5)

        plt.xlim([-83, -65])
        plt.ylim([-5, 15])
        plt.title("Voronoi diagram of Colombian airports")
        plt.show()

    # 2 punto
    def new_airport(self):
        # Distancia, vertice de voronoi, Vertice aeropuerto
        elements = []
        # Vertices de Voronoi
        points_k = []
        # Datos del circulo
        circle = []

        # Puntos y su distancia al vertice de Voronoi
        for i in range(len(self.voronoi.points)):
            dist = []
            for k in range(len(self.voronoi.vertices)):
                dist.append(distance.euclidean(
                    self.voronoi.points[i],
                    self.voronoi.vertices[k]
                    ))
                points_k.append(self.voronoi.vertices[k])
            elements.append((
                min(dist),
                points_k[dist.index(min(dist))],
                self.voronoi.points[i])
                )

        # Datos del circulo
        dist_max = [i[0] for i in elements]
        circle.append(elements[dist_max.index(max(dist_max))])
        circle_center = [circle[0][1]]
        circle_radius = circle[0][0]

        print("Punto 2")
        print("Las coordendas del centro del circulo son: ({0},{1})".format(
            circle_center[0][0],
            circle_center[0][1])
            )
        print("El radio del circulo es: {0}".format(
            circle_radius)
            )

        # Diagrama de Voronoi
        voronoi_plot_2d(
            self.voronoi,
            show_vertices=False,
            show_points=False,
            line_colors='indigo',
            line_alpha=0.4
            )

        # Convex hull
        for simplex in self.hull.simplices:
            plt.plot(
                self.voronoi.points[simplex, 0],
                self.voronoi.points[simplex, 1],
                'b',
                alpha=0.6
                )

        # Aeropuertos
        plt.scatter(
            self.voronoi.points[:, 0],
            self.voronoi.points[:, 1],
            marker="o",
            s=6,
            color="red",
            alpha=0.9
            )

        # Colombia
        plt.plot(self.borders[:, 0], self.borders[:, 1], 'k', alpha=0.5)

        # Circulo
        draw_circle = plt.Circle(
            (circle_center[0][0], circle_center[0][1]),
            circle_radius,
            fill=False
            )
        plt.gcf().gca().add_artist(draw_circle)

        plt.title("Largest circle")
        plt.show()

    # 3 punto
    def pair_airports(self):
        # Puntos comparados
        points_i = []
        points_k = []
        # Distancias
        distances = []
        # Aeropuertos cercanos y lejanos
        farthest_airport = []
        closest_airport = []

        # Distancias y puntos comparados
        for i in range(len(self.voronoi.points)-1):
            for k in range(i+1, len(self.voronoi.points)):
                dist = distance.euclidean(
                    self.voronoi.points[i],
                    self.voronoi.points[k]
                    )
                distances.append(dist)
                points_i.append(self.voronoi.points[i])
                points_k.append(self.voronoi.points[k])

        # Indices de los puntos lejanos y cercanos en la lista de distancias
        index_max = distances.index(max(distances))
        index_min = distances.index(min(distances))

        # Lista con los aeropuertos lejanos y cercanos
        farthest_airport.append(points_i[index_max])
        farthest_airport.append(points_k[index_max])
        closest_airport.append(points_i[index_min])
        closest_airport.append(points_k[index_min])
        farthest_airport = np.array(farthest_airport)
        closest_airport = np.array(closest_airport)

        # Indices de los puntos cercanos y lejanos en los datos originales
        a_L_1, j = np.where(np.isclose(
            self.voronoi.points,
            points_i[index_max])
            )
        a_L_2, j = np.where(np.isclose(
            self.voronoi.points,
            points_k[index_max])
            )
        a_C_1, j = np.where(np.isclose(
            self.voronoi.points,
            points_i[index_min])
            )
        a_C_2, j = np.where(np.isclose(
            self.voronoi.points,
            points_k[index_min])
            )

        print("Punto 3")
        print("Los aeropuertos mas cercanos son: {0} y {1}".format(
            self.airport_info[a_C_1[0]][2],
            self.airport_info[a_C_2[0]][2])
            )
        print("Los aeropuertos mas lejanos son: {0} y {1} ".format(
            self.airport_info[a_L_1[0]][2],
            self.airport_info[a_L_2[0]][2])
            )

        # Graficas con nombres de los aeropuertos mas cercanos y mas lejanos
        plt.plot(self.borders[:, 0], self.borders[:, 1], 'k', alpha=0.4)
        pts1 = plt.scatter(
            farthest_airport[:, 0],
            farthest_airport[:, 1],
            marker="o",
            s=10,
            color="red",
            alpha=1
            )
        pts1.set_label('Farthest airports')
        pts2 = plt.scatter(
            closest_airport[:, 0],
            closest_airport[:, 1],
            marker="o",
            s=2,
            color="blue",
            alpha=1
            )
        pts2.set_label('Closest airports')
        plt.text(
            self.voronoi.points[a_L_1[0], 0] - 0.5,
            self.voronoi.points[a_L_1[0], 1] - 0.8,
            "{0}".format(self.airport_info[a_L_1[0]][2])
            )
        plt.text(
            self.voronoi.points[a_L_2[0], 0],
            self.voronoi.points[a_L_2[0], 1] + 0.2,
            "{0}".format(self.airport_info[a_L_2[0]][2]),
            horizontalalignment='center'
            )
        plt.text(
            self.voronoi.points[a_C_1[0], 0] - 0.1,
            self.voronoi.points[a_C_1[0], 1],
            "{0}".format(self.airport_info[a_C_1[0]][2]),
            horizontalalignment='right'
            )
        plt.text(
            self.voronoi.points[a_C_2[0], 0] + 0.1,
            self.voronoi.points[a_C_2[0], 1] - 0.1,
            "{0}".format(self.airport_info[a_C_2[0]][2])
            )
        plt.title("Nearest and farthest pair of airports")
        plt.legend()
        plt.show()

    # 4 punto
    def altitude_flightplan(self, departure, destination, altitude):
        departure = departure.lower()
        destination = destination.lower()

        # Aeropuertos cercanos y lejanos
        indice_dep = 0
        indice_des = 0

        # Listas con plan de vuelo
        points_init = []
        points_plan = []

        # Texto a minuscula
        for i in range(len(self.airport_elevation)):
            self.airport_info[i][2] = self.airport_info[i][2].lower()
            if departure.lower() in self.airport_info[i][2]:
                indice_dep = i
            if destination.lower() in self.airport_info[i][2]:
                indice_des = i

        points_init.append(self.voronoi.points[indice_dep])
        points_plan.append(self.voronoi.points[indice_dep])

        # Aeropuertos a visitar
        for k in range(len(self.voronoi.points)):
            if (self.airport_elevation[k] > altitude and
                    self.voronoi.points[k][1] >
                    self.voronoi.points[indice_dep][1]):
                points_plan.append(self.voronoi.points[k])

        points_init.append(self.voronoi.points[indice_des])
        points_plan.append(self.voronoi.points[indice_des])
        points_plan = np.array(points_plan)
        points_init = np.array(points_init)

        # Diagrama de Voronoi
        voronoi_plot_2d(
            self.voronoi,
            show_vertices=False,
            show_points=False,
            line_colors='indigo',
            line_alpha=0.4
            )

        # Aeropuertos
        plt.scatter(
            self.voronoi.points[:, 0],
            self.voronoi.points[:, 1],
            marker="o",
            s=6,
            color="black",
            alpha=0.9
            )

        # Plan de vuelo
        plt.plot(points_plan[:, 0], points_plan[:, 1], 'r', alpha=0.8)

        # Punto de inicio y de llegada
        plt.scatter(
            points_init[:, 0],
            points_init[:, 1],
            color='yellow',
            alpha=1
            )

        # Colombia
        plt.plot(self.borders[:, 0], self.borders[:, 1], 'k', alpha=0.5)

        plt.title("Altitude based-flight plan")
        plt.show()
