from Tarea2 import FlightPlan


def main():
    col = FlightPlan(Borders, Airports_Coord, Airports_Info)
    col.new_airport()
    col.pair_airports()
    col.altitude_flightplan("El Carano", "Simon Bolivar", 2000)
    col.plot_voronoi()


# Bordes Colombia
fichero = open('borders_CO.dat',)
Borders = []

for lineas in fichero.readlines():
    list = lineas.split()
    list = [float(list[0]), float(list[1])]
    Borders.append(list)

# Aeropuertos Colombia
fichero2 = open('airports_CO.dat',)
# Coordeneadas aeropuertos
Airports_Coord = []
# Altura,nombres,ciudades aeropuertos
Airports_Info = []
lista_3 = []
for lineas in fichero2.readlines():
    list = lineas.split()
    list3 = []
    list3 += map(str, lineas.split('"'))
    list2 = [
        float(list[2]),
        str(list[3]),
        str(list[4]),
        str(list3[5])
        ]
    list = [float(list[0]), float(list[1])]
    Airports_Coord.append(list)
    Airports_Info.append(list2)

fichero.close()
fichero2.close()
main()
