from Tarea import TIN

# Puntos
fichero = open('pts1000c.dat', )
Puntos = []


for lineas in fichero.readlines():
    # listas con elementos x,y,z
    list = lineas.split()
    list = [float(list[0]), float(list[1]), float(list[2])]
    # lista con flotantes x,y,z
    Puntos.append(list)

# Puntos por coordenada
Punto_x = [item[0] for item in Puntos]
Punto_y = [item[1] for item in Puntos]
Punto_z = [item[2] for item in Puntos]


def main():
    # Punto para interpolacion
    points = (2, 5)

    # Instancia de la clase
    Tin1 = TIN(Punto_x, Punto_y, Punto_z)

    # Aplicacion
    # 1.
    #Tin1.plot_surface()
    # 2.
    Tin1.interpolation(points)
    # 3.
    #Tin1.peak_point()
    # 4.
    #Tin1.anti_peak_point()
    # 5.
    #Tin1.dual_graph()


fichero.close()
main()
